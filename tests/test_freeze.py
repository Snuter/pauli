"""Freeze regression tests: validators, gate copy, sanitizer, DB invariants."""

import sqlite3

from pauli import config as C
from pauli import db
from pauli.safety import resources as R
from pauli.web import sanitize as S


def test_ollama_form_strict():
    assert C.validate_ollama_form("http://localhost:11434", "m", "e", "local") == []
    assert C.validate_ollama_form("bad", "", "", "local") != []
    assert C.validate_ollama_form("http://h", "", "e", "cloud") != []


def test_mail_form_all_empty_is_disabled():
    assert C.validate_mail_form("", "", "", "weekly") == []


def test_mail_form_bare_host_is_422():
    assert C.validate_mail_form("a@b.co", "c@d.co", "localhost", "weekly") != []
    assert C.validate_mail_form("a@b.co", "c@d.co", "localhost:1025", "weekly") == []


def test_422_fragment_escapes():
    assert "role=\"alert\"" in C.validation_error_fragment("x<y")


def test_gate_copy_frozen():
    assert R.DISCLAIMER.startswith("Research info only")
    assert R.CRISIS_LINE == "Crisis: call 112"
    assert R.gate_intro("c", 10) != R.gate_intro("c", 15)


def test_sanitize_links_only_allowed():
    assert "europepmc.org" in S.escape_and_linkify("[PMC1]", {"PMC1"})
    assert "href" not in S.escape_and_linkify("[PMC9]", {"PMC1"})
    assert "<b>" not in S.escape_and_linkify("<b>[PMC1]</b>", {"PMC1"})


def test_db_mode_check_and_defaults(tmp_path):
    p = str(tmp_path / "t.db")
    db.init_db(p)
    con = sqlite3.connect(p)
    try:
        assert con.execute("SELECT COUNT(*) FROM sync_state").fetchone()[0] == 1
        try:
            con.execute("INSERT INTO answers(question,answer,mode) VALUES ('q','a','bogus')")
            ok = True
        except sqlite3.IntegrityError:
            ok = False
        assert not ok
    finally:
        con.close()
    # defaults still validate (empty chat model + empty mail = disabled)
    assert C.Settings().validate() == []
