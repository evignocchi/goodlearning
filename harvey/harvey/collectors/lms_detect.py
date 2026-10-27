"""Which learning platform a company's site points to.

Reads the links, scripts and iframes of a page Harvey already downloaded.
A hit means the company has a learning portal on a vendor's host or at a
path only that vendor's software uses. Silence proves nothing: most LMSs sit
behind a login, so this module never reports "no LMS".

Vendor marketing hosts (www.docebo.com) are not tenants: a company linking
to them reads about the product, it does not run it.
"""

import re
from urllib.parse import urlparse

_NOT_A_TENANT = r"(?!(?:www|community|help|support|blog|docs|learn|academy)\.)"


def _tenant(suffix: str) -> re.Pattern:
    return re.compile(rf"https?://{_NOT_A_TENANT}[a-z0-9-]+(?:\.[a-z0-9-]+)*\.{suffix}\b", re.I)


# name -> patterns matched against the raw HTML. A named vendor is 0.9.
VENDORS: dict[str, list[re.Pattern]] = {
    "Docebo": [_tenant(r"docebosaas\.com")],
    "TalentLMS": [_tenant(r"talentlms\.com")],
    "Absorb LMS": [_tenant(r"myabsorb\.com")],
    "Cornerstone": [_tenant(r"csod\.com")],
    "LearnWorlds": [_tenant(r"learnworlds\.com")],
    "Thinkific": [_tenant(r"thinkific\.com")],
    "Teachable": [_tenant(r"teachable\.com")],
    "iSpring Learn": [_tenant(r"ispringlearn\.com")],
    "Litmos": [_tenant(r"litmos\.com")],
    "Canvas": [_tenant(r"instructure\.com")],
    "SAP SuccessFactors": [_tenant(r"successfactors\.(?:com|eu)")],
    "360Learning": [_tenant(r"360learning\.com")],
    "Moodle": [
        re.compile(r"https?://(?!(?:www\.|docs\.|download\.|tracker\.|moodle\.org|moodle\.com))"
                   r"[a-z0-9.-]*moodle[a-z0-9.-]*", re.I),
        re.compile(r"/course/view\.php\?id=\d+", re.I),
        re.compile(r"https?://[^/\s\"']+/moodle/", re.I),
    ],
}

# Their own subdomain named for e-learning (elearning.acme.it, fad.acme.it):
# there is a learning portal, but not which one. Weaker, so 0.5.
_PORTAL_RE = re.compile(r"https?://((?:elearning|e-learning|lms|fad)\.[a-z0-9.-]+)", re.I)
UNIDENTIFIED = "portale e-learning (piattaforma non identificata)"


def _registrable(host: str) -> str:
    parts = host.lower().removeprefix("www.").split(".")
    return ".".join(parts[-2:])


def detect_lms(html: str, domain: str = "") -> list[tuple[str, float]]:
    """Platforms the page links to, as (name, confidence), strongest first."""
    found: dict[str, float] = {}
    for name, patterns in VENDORS.items():
        if any(p.search(html) for p in patterns):
            found[name] = 0.9
    if not found and domain:
        own = _registrable(domain)
        for match in _PORTAL_RE.finditer(html):
            host = urlparse("https://" + match.group(1)).netloc
            if _registrable(host) == own:
                found[UNIDENTIFIED] = 0.5
                break
    return sorted(found.items(), key=lambda kv: -kv[1])
