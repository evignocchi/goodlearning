"""The Goodlearning playbook and product facts reach the agents that need them."""

from pathlib import Path

import pytest
import yaml

from harvey import brain as brain_mod
from harvey.brain import Brain
from harvey.config import HarveyConfig

SKILLS = Path(brain_mod.__file__).resolve().parent.parent / "skills"


def _brain():
    return Brain.__new__(Brain)


@pytest.mark.parametrize("agent", ["scout", "writer", "handler"])
def test_agents_load_the_goodlearning_context(agent):
    text = _brain().load_skills_for_agent(agent)
    assert "Goodlearning: conoscenza del prodotto" in text
    assert "Goodlearning: a chi scrivere" in text


@pytest.mark.parametrize("agent", ["scout", "writer"])
def test_scout_and_writer_get_the_use_cases(agent):
    assert "casi d'uso, formazioni obbligatorie" in _brain().load_skills_for_agent(agent)


def test_use_cases_file_warns_that_legal_details_are_unverified():
    text = (SKILLS / "goodlearning_use_cases.md").read_text()
    assert "non verificati" in text


def test_sender_gets_the_facts_but_not_the_internal_playbook():
    text = _brain().load_skills_for_agent("sender")
    assert "Goodlearning: conoscenza del prodotto" in text
    assert "Goodlearning: a chi scrivere" not in text


def test_every_catalog_signal_named_in_the_playbook_exists():
    import re
    from harvey.signals import SIGNAL_CATALOG
    codes = {s["code"] for s in SIGNAL_CATALOG}
    named = set(re.findall(r"`([A-Z][A-Z_]{3,})`", (SKILLS / "goodlearning_playbook.md").read_text() + (SKILLS / "goodlearning_use_cases.md").read_text()))
    assert named and named <= codes


def test_local_config_describes_goodlearning_and_still_validates():
    data = yaml.safe_load((SKILLS.parent / "harvey.local.yaml").read_text())
    config = HarveyConfig(**data)
    assert config.product.name == "Goodlearning"
    assert "RSPP" in config.icp.titles
    assert config.icp.geography == ["Lombardia"]
