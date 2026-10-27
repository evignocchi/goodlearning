"""Lead-list import — CSV exports (Apollo and similar) into Harvey's database.

Two steps so the dedup report can be read before anything is written:

* ``plan_import`` parses and normalises the file and removes duplicates
  inside it. It touches no database.
* ``apply_import`` checks the survivors against what Harvey already holds
  and inserts the rest.

Dedup keys, strongest first: email, LinkedIn URL, then name + company.
"""

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from harvey.models.company import Company
from harvey.models.prospect import Prospect
from harvey.state import FREE_MAIL_DOMAINS, StateManager

IMPORT_SOURCE = "import"

# Header aliases, lowercased. First match wins.
COLUMNS = {
    "full_name": ("full name", "name", "contact name"),
    "first_name": ("first name", "firstname"),
    "last_name": ("last name", "lastname"),
    "title": ("job title", "title", "position"),
    "company": ("company", "company name", "organization", "company name for emails"),
    "city": ("city",),
    "region": ("region", "state"),
    "country": ("country",),
    "employees": ("employees", "# employees", "company size"),
    "industry": ("industry",),
    "email": ("email", "work email", "email address"),
    "phone": ("phone", "mobile phone", "work direct phone", "corporate phone"),
    "website": ("website", "company website", "domain"),
    "linkedin": ("linkedin", "person linkedin url", "linkedin url", "linkedin_url"),
}

_PHONE_NOTE = re.compile(r"\s*\(.*?\)\s*$")


@dataclass
class Lead:
    first_name: str
    last_name: str
    title: str
    company: str
    email: str = ""
    phone: str = ""
    linkedin_url: str = ""
    domain: str = ""
    industry: str = ""
    employees: str = ""
    location: str = ""
    seniority: str = ""
    row: int = 0

    def name_key(self) -> tuple[str, str, str]:
        return (self.first_name.lower(), self.last_name.lower(), _company_key(self.company))


@dataclass
class ImportPlan:
    leads: list[Lead] = field(default_factory=list)
    rows: int = 0
    skipped: list[tuple[int, str]] = field(default_factory=list)       # (row, reason)
    duplicates: list[tuple[int, str]] = field(default_factory=list)    # (row, why)
    shared_phones: list[tuple[int, str]] = field(default_factory=list) # (row, phone dropped)


@dataclass
class ImportResult:
    plan: ImportPlan
    inserted: int = 0
    existing: list[tuple[int, str]] = field(default_factory=list)
    without_email: int = 0


def _company_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def normalize_linkedin(url: str) -> str:
    """Canonical ``https://www.linkedin.com/in/<slug>`` so tracking
    parameters and trailing slashes do not hide a duplicate."""
    url = (url or "").strip()
    if not url:
        return ""
    if "://" not in url:
        url = "https://" + url
    parsed = urlparse(url)
    if "linkedin.com" not in parsed.netloc.lower():
        return ""
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2 or parts[0].lower() not in ("in", "pub"):
        return ""
    return f"https://www.linkedin.com/{parts[0].lower()}/{parts[1].lower()}"


def normalize_phone(raw: str) -> str:
    """Keep ``+`` and digits; the trailing note (``(company switchboard)``) goes."""
    raw = _PHONE_NOTE.sub("", raw or "")
    digits = re.sub(r"[^\d+]", "", raw)
    return digits if len(digits) >= 7 else ""


def domain_of(email: str = "", website: str = "") -> str:
    """Company domain from a website if given, else from the email address.
    Free-mail domains say nothing about the company and give ''."""
    site = (website or "").strip().lower()
    if site:
        site = urlparse(site if "://" in site else "https://" + site).netloc
        site = site.removeprefix("www.")
        if site and "." in site:
            return site
    if "@" in email:
        domain = email.rsplit("@", 1)[1].strip().lower()
        if domain and domain not in FREE_MAIL_DOMAINS:
            return domain
    return ""


def seniority_of(title: str) -> str:
    t = title.lower()
    if re.search(r"\b(ceo|chairman|president|presidente|amministratore delegato|"
                 r"direttore generale|general manager|co-?founder|managing director)\b", t):
        return "c_suite"
    if re.search(r"\b(vp|vice president)\b", t):
        return "vp"
    if re.search(r"\b(director|direttore|head of|head)\b", t):
        return "director"
    if re.search(r"\b(manager|responsabile)\b", t):
        return "manager"
    return "individual"


def _split_name(full: str) -> tuple[str, str]:
    parts = full.split()
    if len(parts) < 2:
        return (parts[0] if parts else "", "")
    return parts[0], " ".join(parts[1:])


def _column_map(headers: list[str]) -> dict[str, str]:
    lowered = {h.strip().lower(): h for h in headers}
    found = {}
    for key, aliases in COLUMNS.items():
        for alias in aliases:
            if alias in lowered:
                found[key] = lowered[alias]
                break
    return found


def plan_import(path: str | Path) -> ImportPlan:
    plan = ImportPlan()
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = _column_map(reader.fieldnames or [])
        if "email" not in cols and "linkedin" not in cols:
            raise ValueError("the file needs an Email or a LinkedIn URL column")
        if "full_name" not in cols and not ("first_name" in cols and "last_name" in cols):
            raise ValueError("the file needs a Full Name, or First Name and Last Name")
        rows = list(reader)

    def get(row: dict, key: str) -> str:
        col = cols.get(key)
        return (row.get(col) or "").strip() if col else ""

    seen_email: dict[str, int] = {}
    seen_linkedin: dict[str, int] = {}
    seen_name: dict[tuple, int] = {}
    phone_owners: dict[str, list[Lead]] = {}

    for i, row in enumerate(rows, start=2):  # row 1 is the header
        plan.rows += 1
        if "full_name" in cols and get(row, "full_name"):
            first, last = _split_name(get(row, "full_name"))
        else:
            first, last = get(row, "first_name"), get(row, "last_name")
        title, company = get(row, "title"), get(row, "company")
        if not (first and last):
            plan.skipped.append((i, "no first and last name"))
            continue
        if not title:
            plan.skipped.append((i, "no job title"))
            continue
        if not company:
            plan.skipped.append((i, "no company"))
            continue

        email = get(row, "email").lower()
        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            email = ""
        location = ", ".join(x for x in (get(row, "city"), get(row, "region"),
                                         get(row, "country")) if x)
        lead = Lead(
            first_name=first, last_name=last, title=title, company=company,
            email=email, phone=normalize_phone(get(row, "phone")),
            linkedin_url=normalize_linkedin(get(row, "linkedin")),
            domain=domain_of(email, get(row, "website")),
            industry=get(row, "industry"), employees=get(row, "employees"),
            location=location, seniority=seniority_of(title), row=i,
        )

        if lead.email and lead.email in seen_email:
            plan.duplicates.append((i, f"same email as row {seen_email[lead.email]}"))
            continue
        if lead.linkedin_url and lead.linkedin_url in seen_linkedin:
            plan.duplicates.append((i, f"same LinkedIn as row {seen_linkedin[lead.linkedin_url]}"))
            continue
        if lead.name_key() in seen_name:
            plan.duplicates.append((i, f"same name and company as row {seen_name[lead.name_key()]}"))
            continue
        if lead.email:
            seen_email[lead.email] = i
        if lead.linkedin_url:
            seen_linkedin[lead.linkedin_url] = i
        seen_name[lead.name_key()] = i
        if lead.phone:
            phone_owners.setdefault(lead.phone, []).append(lead)
        plan.leads.append(lead)

    # One number on people at different companies is a data error, not a
    # shared line: calling it a contact detail would mislead.
    for phone, owners in phone_owners.items():
        if len({_company_key(o.company) for o in owners}) > 1:
            for o in owners:
                o.phone = ""
                plan.shared_phones.append((o.row, phone))
    return plan


def _notes(lead: Lead) -> str:
    bits = []
    if lead.location:
        bits.append(f"based in {lead.location}")
    if lead.employees:
        bits.append(f"about {lead.employees} employees")
    return ("Imported lead: " + "; ".join(bits)) if bits else ""


async def apply_import(state: StateManager, plan: ImportPlan) -> ImportResult:
    result = ImportResult(plan=plan)
    companies: dict[str, str] = {}  # company key -> id, within this run
    for lead in plan.leads:
        if await state.prospect_exists(
            email=lead.email, linkedin_url=lead.linkedin_url,
            first_name=lead.first_name, last_name=lead.last_name, company=lead.company,
        ):
            result.existing.append((lead.row, f"{lead.first_name} {lead.last_name}"))
            continue

        key = lead.domain or _company_key(lead.company)
        if key not in companies:
            companies[key] = await state.add_company(Company(
                name=lead.company, domain=lead.domain,
                website=f"https://{lead.domain}" if lead.domain else "",
                industry=lead.industry, company_size=lead.employees,
                location=lead.location, source=IMPORT_SOURCE,
                external_id="" if lead.domain else f"{IMPORT_SOURCE}:{_company_key(lead.company)}",
            ))
        await state.add_prospect(Prospect(
            company_id=companies[key], first_name=lead.first_name,
            last_name=lead.last_name, email=lead.email, phone=lead.phone,
            linkedin_url=lead.linkedin_url, title=lead.title,
            seniority=lead.seniority, source=IMPORT_SOURCE,
            personalization_notes=_notes(lead), company=lead.company,
            industry=lead.industry, company_size=lead.employees,
        ))
        result.inserted += 1
        if not lead.email:
            result.without_email += 1
    return result


def format_report(plan: ImportPlan, result: ImportResult | None = None) -> str:
    lines = [f"  Rows read:           {plan.rows}",
             f"  Skipped (invalid):   {len(plan.skipped)}",
             f"  Duplicates in file:  {len(plan.duplicates)}",
             f"  Unique leads:        {len(plan.leads)}",
             f"  Without email:       {sum(1 for l in plan.leads if not l.email)}",
             f"  Phone dropped:       {len(plan.shared_phones)} (one number on different companies)"]
    if result:
        lines += [f"  Already in Harvey:   {len(result.existing)}",
                  f"  Imported:            {result.inserted}"]
    for title, items in (("Skipped", plan.skipped), ("Duplicates", plan.duplicates),
                         ("Phone dropped", plan.shared_phones)):
        for row, why in items:
            lines.append(f"    {title}, row {row}: {why}")
    if result:
        for row, name in result.existing:
            lines.append(f"    Already known, row {row}: {name}")
    return "\n".join(lines)
