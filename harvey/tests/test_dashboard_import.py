"""Importing a lead list from the dashboard: preview first, then import."""

import asyncio
import sqlite3

import pytest
from fastapi.testclient import TestClient

import harvey.dashboard as dash
from harvey.state import StateManager

ORIGIN = "http://127.0.0.1:5555"
CSV = (
    "Full Name,Job Title,Company,City,Region,Employees,Industry,Email,Phone\n"
    "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,jo@acme.test,\n"
    "Jo Li,HR Manager,Acme Srl,Milan,Lombardy,100,Machinery,JO@ACME.TEST,\n"
    "Sam Ro,CEO,Beta Spa,Como,Lombardy,50,Chemicals,,\n"
)


@pytest.fixture
def env(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    db = tmp_path / "data" / "harvey.db"
    monkeypatch.setattr(dash, "ENV_FILE", tmp_path / ".env")
    monkeypatch.setattr(dash, "DB_PATH", db)
    monkeypatch.setattr(dash, "PID_FILE", tmp_path / "data" / "harvey.pid")
    monkeypatch.setattr(dash, "LOG_FILE", tmp_path / "data" / "harvey.log")
    dash.token_store.configure(tmp_path / "data" / "dashboard-token")
    asyncio.run(StateManager(db_path=str(db)).init_db())
    return {"db": db, "token": dash.token_store.get()}


@pytest.fixture
def client(env):
    with TestClient(dash.app, base_url=ORIGIN,
                    headers={"Authorization": f"Bearer {env['token']}"}) as c:
        yield c


def _count(env):
    with sqlite3.connect(env["db"]) as db:
        return db.execute("SELECT COUNT(*) FROM prospects").fetchone()[0]


def test_preview_reports_and_writes_nothing(client, env):
    r = client.post("/api/import/preview", json={"text": CSV})
    assert r.status_code == 200
    body = r.json()
    assert (body["rows"], body["unique"], body["without_email"]) == (3, 2, 1)
    assert [d["row"] for d in body["duplicates"]] == [3]
    assert _count(env) == 0


def test_apply_imports_once_and_then_knows_them(client, env):
    first = client.post("/api/import/apply", json={"text": CSV}).json()
    assert first["imported"] == 2 and first["email_status"] == "verified"
    assert _count(env) == 2
    with sqlite3.connect(env["db"]) as db:
        assert db.execute("SELECT email_status FROM prospects WHERE email = 'jo@acme.test'"
                          ).fetchone()[0] == "verified"

    preview = client.post("/api/import/preview", json={"text": CSV}).json()
    assert len(preview["known"]) == 2
    again = client.post("/api/import/apply", json={"text": CSV}).json()
    assert again["imported"] == 0 and _count(env) == 2


def test_email_status_can_be_chosen(client, env):
    client.post("/api/import/apply", json={"text": CSV, "email_status": "guess"})
    with sqlite3.connect(env["db"]) as db:
        assert db.execute("SELECT email_status FROM prospects WHERE email = 'jo@acme.test'"
                          ).fetchone()[0] == "guess"


@pytest.mark.parametrize("payload,code", [
    ({}, 400), ({"text": ""}, 400), ({"text": 5}, 400),
    ({"text": "Foo,Bar\n1,2\n"}, 400),                       # no name/email columns
    ({"text": CSV, "email_status": "great"}, 400),
])
def test_bad_uploads_are_refused(client, env, payload, code):
    assert client.post("/api/import/apply", json=payload).status_code == code
    assert _count(env) == 0


def test_a_huge_upload_is_refused(client, monkeypatch):
    monkeypatch.setattr(dash, "MAX_IMPORT_CHARS", 50)
    assert client.post("/api/import/preview", json={"text": CSV}).status_code == 413


def test_import_needs_the_token(env):
    with TestClient(dash.app, base_url=ORIGIN) as anon:
        assert anon.post("/api/import/preview", json={"text": CSV}).status_code in (401, 403)


def test_outbox_says_when_the_user_sends_by_hand(client, monkeypatch):
    monkeypatch.setattr(dash, "_harvey_can_send", lambda: False)
    assert client.get("/api/outbox").json()["by_hand"] is True
    monkeypatch.setattr(dash, "_harvey_can_send", lambda: True)
    assert client.get("/api/outbox").json()["by_hand"] is False
