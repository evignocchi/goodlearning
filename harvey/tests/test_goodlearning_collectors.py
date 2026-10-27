"""LMS and certification detection: what counts as a claim, and what never does."""

import os
import tempfile

import pytest
import pytest_asyncio

from harvey.collectors.cert_detect import detect_certifications
from harvey.collectors.lms_detect import UNIDENTIFIED, detect_lms
from harvey.collectors.profile import ProfileCollector
from harvey.models.company import Company
from harvey.state import StateManager


# ── LMS ──

@pytest.mark.parametrize("html,name", [
    ('<a href="https://acme.docebosaas.com/learn">Academy</a>', "Docebo"),
    ('<a href="https://acme.talentlms.com">Corsi</a>', "TalentLMS"),
    ('<a href="https://learning.acme.example/moodle/login">Login</a>', "Moodle"),
    ('<a href="/course/view.php?id=42">Corso</a>', "Moodle"),
    ('<iframe src="https://acme.360learning.com/x"></iframe>', "360Learning"),
])
def test_a_link_to_a_tenant_names_the_platform(html, name):
    assert detect_lms(html, "acme.example") == [(name, 0.9)]


@pytest.mark.parametrize("html", [
    '<a href="https://www.docebo.com/it/">Docebo</a>',               # vendor marketing site
    '<a href="https://moodle.org/">Moodle</a>',
    '<a href="https://www.talentlms.com/pricing">TalentLMS</a>',
    "<p>Usiamo Moodle ogni giorno.</p>",                              # a word is not a link
    "",
])
def test_vendor_sites_and_plain_words_are_not_tenants(html):
    assert detect_lms(html, "acme.example") == []


def test_own_elearning_subdomain_is_an_unidentified_portal():
    html = '<a href="https://elearning.acme.example/login">Area corsi</a>'
    assert detect_lms(html, "acme.example") == [(UNIDENTIFIED, 0.5)]
    assert detect_lms(html, "www.acme.example") == [(UNIDENTIFIED, 0.5)]


def test_somebody_elses_elearning_subdomain_is_ignored():
    assert detect_lms('<a href="https://lms.other.example/">x</a>', "acme.example") == []


def test_a_named_vendor_beats_the_unidentified_portal():
    html = ('<a href="https://elearning.acme.example/">a</a>'
            '<a href="https://acme.talentlms.com">b</a>')
    assert detect_lms(html, "acme.example") == [("TalentLMS", 0.9)]


# ── certifications ──

@pytest.mark.parametrize("text,label", [
    ("Siamo un'azienda certificata ISO 9001 dal 2011.", "ISO 9001"),
    ("Certificazioni: UNI EN ISO 14001 rinnovata nel 2024.", "ISO 14001"),
    ("We are ISO 45001 certified.", "ISO 45001"),
    ("Sistema di gestione conforme alla norma IATF 16949.", "IATF 16949"),
    ("Qualità: certificazione ISO/IEC 27001 per la sicurezza delle informazioni.", "ISO 27001"),
])
def test_a_stated_claim_counts(text, label):
    assert detect_certifications(text) == [(label, 0.85)]


@pytest.mark.parametrize("text", [
    "Offriamo consulenza per ottenere la certificazione ISO 9001.",
    "Corso ISO 45001 per responsabili della sicurezza.",
    "Ti aiutiamo a implementare ISO 27001 in azienda.",
    "ISO 9001",                                                   # bare mention, no claim
    "Il nostro catalogo comprende 90010 articoli.",
    "",
])
def test_offers_and_bare_mentions_do_not_count(text):
    assert detect_certifications(text) == []


def test_a_corsi_menu_link_next_to_a_claim_does_not_cancel_it():
    text = "Home Prodotti Corsi Contatti Azienda certificata ISO 9001 dal 2011."
    assert detect_certifications(text) == [("ISO 9001", 0.85)]


def test_several_standards_come_back_one_each():
    text = "Certificati ISO 9001 e ISO 14001. Certificata anche ISO 9001 per la sede di Como."
    assert sorted(l for l, _ in detect_certifications(text)) == ["ISO 14001", "ISO 9001"]


# ── through the profile collector ──

@pytest_asyncio.fixture
async def state():
    with tempfile.TemporaryDirectory() as tmp:
        sm = StateManager(os.path.join(tmp, "t.db"))
        await sm.init_db()
        yield sm


HOME = ("<html><body>" + "<p>Presentazione dell'azienda.</p>" * 30 +
        '<a href="https://acme.talentlms.com">Corsi</a>'
        "<p>Azienda certificata ISO 9001.</p></body></html>")
QUALITY = ("<html><body>" + "<p>Politica per la qualità.</p>" * 30 +
           "<p>Certificazione ISO 45001 ottenuta nel 2023.</p></body></html>")


def _collector(confirmed, state):
    c = ProfileCollector.__new__(ProfileCollector)
    c.confirmed = set(confirmed)
    c.site_names = {}
    c.role_keywords = []
    c.challenged = set()
    c.state = state

    async def fake_get(url):
        return {"https://acme.example": HOME, "https://acme.example/qualita": QUALITY}.get(url.rstrip("/"), "")

    async def resolve(domain):
        return "https://acme.example", HOME
    c._get = fake_get
    c._resolve_site = resolve
    return c


@pytest.mark.asyncio
async def test_confirmed_signals_come_back_with_their_evidence(state):
    cid = await state.add_company(Company(name="Acme", domain="acme.example"))
    obs = await _collector({"LMS_IN_USE", "CERT_ISO"}, state).profile_company(cid, "acme.example")
    got = {(o["signal_code"], o["value_text"], o["evidence_url"]) for o in obs}
    assert got == {
        ("LMS_IN_USE", "TalentLMS", "https://acme.example"),
        ("CERT_ISO", "ISO 9001", "https://acme.example"),
        ("CERT_ISO", "ISO 45001", "https://acme.example/qualita"),
    }


@pytest.mark.asyncio
async def test_unconfirmed_signals_are_not_collected(state):
    cid = await state.add_company(Company(name="Acme", domain="acme.example"))
    obs = await _collector(set(), state).profile_company(cid, "acme.example")
    assert not {o["signal_code"] for o in obs} & {"LMS_IN_USE", "CERT_ISO"}


@pytest.mark.asyncio
async def test_a_site_that_says_nothing_records_nothing(state, monkeypatch):
    cid = await state.add_company(Company(name="Acme", domain="acme.example"))
    c = _collector({"LMS_IN_USE", "CERT_ISO"}, state)

    async def resolve(domain):
        return "https://acme.example", "<html>" + "<p>Ciao.</p>" * 60 + "</html>"

    async def nothing(url):
        return ""
    c._resolve_site, c._get = resolve, nothing
    assert await c.profile_company(cid, "acme.example") == []
