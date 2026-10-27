"""Certifications a company says it holds, from the text of its own pages.

A standard's name next to a claim ("certificata ISO 9001", "we are ISO 45001
certified") counts. The same name next to an offer to help others get it
("consulenza ISO 9001", "corso ISO 45001") does not, and neither does a bare
mention. Logos are images and cannot be read, so silence proves nothing: this
module only reports what a page states.
"""

import re

# label -> pattern for the standard's name
STANDARDS: dict[str, str] = {
    "ISO 9001": r"ISO\s*9001",
    "ISO 14001": r"ISO\s*14001",
    "ISO 45001": r"ISO\s*45001|OHSAS\s*18001",
    "ISO 27001": r"ISO\s*(?:/IEC\s*)?27001",
    "ISO 37001": r"ISO\s*37001",
    "ISO 22000": r"ISO\s*22000",
    "ISO 13485": r"ISO\s*13485",
    "ISO 50001": r"ISO\s*50001",
    "ISO 3834": r"ISO\s*3834",
    "ISO 22716": r"ISO\s*22716",
    "IATF 16949": r"IATF\s*16949",
    "AS9100": r"\bAS\s*9100|EN\s*9100",
    "SA8000": r"\bSA\s*8000",
    "UNI/PdR 125": r"UNI\s*/?\s*PdR\s*125",
    "BRCGS": r"\bBRC(?:GS)?\b|BRC\s+Global\s+Standard",
    "IFS": r"\bIFS\s+(?:Food|Logistics|HPC)\b",
}
_COMPILED = {label: re.compile(rf"(?<![\w/])(?:{p})", re.I) for label, p in STANDARDS.items()}

# A claim: the company says it holds it.
_CLAIM = re.compile(
    r"certificat[aoie]|certified|certification|certificazion|conform[ei]\s+(?:alla|alle|ai)\s+(?:norma|norme|standard)"
    r"|accreditat|ottenut[ao]|rinnovat[ao]|\bUNI\s+EN\b", re.I)
# An offer to help someone else get it: the offer's noun sits right before or
# after the standard ("corso ISO 45001", "consulenza per la certificazione
# ISO 9001"), or the sentence talks about getting it ("ti aiutiamo a ottenere").
# A "Corsi" menu link elsewhere in the same text is not an offer.
_FILLER = r"(?:\s+(?:di|su|per|sulla|sulle|alla|alle|in|dell'|della|la|il|lo|l'|norma|certificazione|uni|en))*"
_OFFER_NOUN = r"(?:consulenza|consulenti|consulting|corso|corsi|course|courses|training|formazione|implementazione|audit)"
_OFFER_BEFORE = re.compile(rf"{_OFFER_NOUN}{_FILLER}\s*$", re.I)
_OFFER_AFTER = re.compile(rf"\s*{_OFFER_NOUN}\b", re.I)
_OFFER_VERB = re.compile(r"ti\s+aiut|vi\s+aiut|ottien[ie]|ottenere|implementare|implementazion", re.I)
WINDOW = 120
CONFIDENCE = 0.85


def detect_certifications(text: str) -> list[tuple[str, float]]:
    """Standards a page claims, as (label, confidence)."""
    found: dict[str, float] = {}
    for label, pattern in _COMPILED.items():
        for match in pattern.finditer(text):
            around = text[max(0, match.start() - WINDOW): match.end() + WINDOW]
            before = text[max(0, match.start() - 60): match.start()]
            after = text[match.end(): match.end() + 30]
            sentence = re.split(r"[.!?;|]", around)
            here = next((x for x in sentence if pattern.search(x)), "")
            offer = (_OFFER_BEFORE.search(before) or _OFFER_AFTER.match(after)
                     or _OFFER_VERB.search(here))
            if _CLAIM.search(around) and not offer:
                found[label] = CONFIDENCE
                break
    return list(found.items())
