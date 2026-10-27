"""Lead-list import: normalisation, dedup inside the file and against Harvey's database."""

import pytest

from harvey.importer import (
    apply_import, domain_of, normalize_linkedin, normalize_phone, plan_import, seniority_of,
)
from harvey.state import StateManager

HEADER = "Full Name,Job Title,Company,City,Region,Employees,Industry,Email,Phone,Person Linkedin Url\n"


def write(tmp_path, *rows):
    path = tmp_path / "leads.csv"
    path.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_normalizers():
    assert normalize_linkedin("linkedin.com/in/Jo-Li/?utm=x") == "https://www.linkedin.com/in/jo-li"
    assert normalize_linkedin("https://example.com/in/jo") == ""
    assert normalize_phone("+39 02 1234567 (company switchboard)") == "+39021234567"
    assert normalize_phone("123") == ""
    assert domain_of("jo@acme.test") == "acme.test"
    assert domain_of("jo@gmail.com") == ""
    assert domain_of("jo@gmail.com", "https://www.acme.test/about") == "acme.test"
    assert seniority_of("HR Director") == "director"
    assert seniority_of("Amministratore Delegato") == "c_suite"
    assert seniority_of("HSE Manager") == "manager"


def test_dedup_inside_the_file(tmp_path):
    plan = plan_import(write(
        tmp_path,
        "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,jo@acme.test,+390211111111,",
        "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,JO@ACME.TEST,,",          # same email
        "Joan Li,HR Manager,Acme,Milan,Lombardy,100,Machinery,,,https://www.linkedin.com/in/jl/",
        "Joan Li,HR,Acme,Milan,Lombardy,100,Machinery,,,linkedin.com/in/jl?x=1",           # same LinkedIn
        "Sam Ro,CEO,Beta Spa,Como,Lombardy,50,Chemicals,,,",
        "sam ro,CEO,BETA S.p.A.,Como,Lombardy,50,Chemicals,sam@beta.test,,",               # same name+company
    ))
    assert plan.rows == 6
    assert [l.first_name for l in plan.leads] == ["Jo", "Joan", "Sam"]
    assert len(plan.duplicates) == 3


def test_invalid_rows_are_reported_not_imported(tmp_path):
    plan = plan_import(write(
        tmp_path,
        "Cher,CEO,Acme,,,,,,,",                        # one-word name
        "Jo Li,,Acme,,,,,jo@acme.test,,",              # no title
        "Jo Li,CEO,,,,,,jo@acme.test,,",               # no company
        "Jo Li,CEO,Acme,,,,,not-an-email,,",           # bad email: kept, email dropped
    ))
    assert len(plan.skipped) == 3
    assert plan.leads[0].email == ""


def test_phone_shared_across_companies_is_dropped(tmp_path):
    plan = plan_import(write(
        tmp_path,
        "Jo Li,CEO,Acme,,,,,jo@acme.test,+390211111111,",
        "Sam Ro,CEO,Beta,,,,,sam@beta.test,+390211111111,",
        "Ann Bo,CFO,Beta,,,,,ann@beta.test,+390222222222,",
        "Tim Re,CTO,Beta,,,,,tim@beta.test,+390222222222,",   # same company: a real shared line
    ))
    phones = {l.first_name: l.phone for l in plan.leads}
    assert phones == {"Jo": "", "Sam": "", "Ann": "+390222222222", "Tim": "+390222222222"}
    assert len(plan.shared_phones) == 2


def test_missing_required_columns(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("Foo,Bar\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        plan_import(path)


@pytest.mark.asyncio
async def test_apply_is_idempotent_and_groups_companies(tmp_path):
    path = write(
        tmp_path,
        "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,jo@acme.test,,",
        "Ann Bo,CEO,Acme Srl,Milan,Lombardy,100,Machinery,ann@acme.test,,",
        "Sam Ro,CEO,Beta Spa,Como,Lombardy,50,Chemicals,,,",
    )
    state = StateManager(str(tmp_path / "h.db"))
    await state.init_db()

    first = await apply_import(state, plan_import(path))
    assert first.inserted == 3 and first.without_email == 1 and not first.existing

    again = await apply_import(state, plan_import(path))
    assert again.inserted == 0 and len(again.existing) == 3

    jo = await state.get_prospect_by_email("jo@acme.test")
    ann = await state.get_prospect_by_email("ann@acme.test")
    assert jo.company_id == ann.company_id
    assert jo.seniority == "manager" and jo.source == "import"
    assert "Milan, Lombardy" in jo.personalization_notes
    company = await state.get_company(jo.company_id)
    assert company.domain == "acme.test"


@pytest.mark.asyncio
async def test_addresses_are_verified_on_import_by_default(tmp_path):
    path = write(
        tmp_path,
        "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,jo@acme.test,,",
        "Sam Ro,CEO,Beta Spa,Como,Lombardy,50,Chemicals,,,",
    )
    state = StateManager(str(tmp_path / "h.db"))
    await state.init_db()
    result = await apply_import(state, plan_import(path))
    assert result.email_status == "verified"
    jo = await state.get_prospect_by_email("jo@acme.test")
    assert jo.email_status == "verified" and jo.email_verified
    assert len(await state.get_prospects_by_status("new")) == 2   # the one without email stays unwritable


@pytest.mark.asyncio
async def test_email_status_can_be_set_to_guess(tmp_path):
    path = write(tmp_path, "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,jo@acme.test,,")
    state = StateManager(str(tmp_path / "h.db"))
    await state.init_db()
    await apply_import(state, plan_import(path), email_status="guess")
    jo = await state.get_prospect_by_email("jo@acme.test")
    assert jo.email_status == "guess" and not jo.email_verified
