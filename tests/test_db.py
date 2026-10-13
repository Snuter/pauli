"""Phase S4 verify: canonical schema, idempotent init, no topic_hash."""

import sqlite3

from pauli import db


def test_init_and_tables(tmp_path):
    p = str(tmp_path / "pauli.db")
    db.init_db(p)
    db.init_db(p)  # idempotent
    con = sqlite3.connect(p)
    try:
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        for t in ("papers", "chunks", "answers", "sessions", "session_answers", "sync_state", "warning_events"):
            assert t in tables
        cols = [r[1] for r in con.execute("PRAGMA table_info(chunks)")]
        assert "topic_hash" not in cols
        # UNIQUE title enforced
        con.execute("INSERT INTO sessions(id,title,created_at) VALUES ('a','T',1)")
        try:
            con.execute("INSERT INTO sessions(id,title,created_at) VALUES ('b','T',2)")
            committed = True
        except sqlite3.IntegrityError:
            committed = False
        assert not committed
    finally:
        con.close()


def test_no_topic_hash_in_schema():
    assert "topic_hash" not in db.SCHEMA_SQL
