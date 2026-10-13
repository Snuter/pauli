"""Canonical SQLite schema (Phase S4) — single shared global corpus.

No ``topic_hash`` anywhere (dropped 2026-10-12). Retrieval is global.
``chunks.vec`` is the sqlite-vec vector column (embedding dim depends on
``OLLAMA_EMBED_MODEL``); ``vectors`` count = ``chunks`` count.
"""

from __future__ import annotations

import sqlite3

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS papers (
  pmcid TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  year INTEGER,
  authors TEXT NOT NULL DEFAULT '',
  url TEXT NOT NULL DEFAULT '',
  abstract TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pmcid TEXT NOT NULL REFERENCES papers(pmcid) ON DELETE CASCADE,
  idx INTEGER NOT NULL,
  text TEXT NOT NULL,
  vec BLOB NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chunks_pmcid ON chunks(pmcid);
CREATE TABLE IF NOT EXISTS answers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  answer TEXT NOT NULL DEFAULT '',
  mode TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL UNIQUE,
  created_at INTEGER NOT NULL,
  subscribed INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS session_answers (
  session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  question TEXT NOT NULL,
  answer_id INTEGER REFERENCES answers(id) ON DELETE SET NULL,
  position INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_session_answers_session ON session_answers(session_id);
CREATE TABLE IF NOT EXISTS sync_state (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  last_run TEXT
);
CREATE TABLE IF NOT EXISTS warning_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,
  action TEXT NOT NULL,
  mode TEXT NOT NULL DEFAULT '',
  at TEXT NOT NULL DEFAULT ''
);
"""


def init_db(path: str) -> None:
    """Create all tables. Idempotent."""
    con = sqlite3.connect(path)
    try:
        con.executescript(SCHEMA_SQL)
        con.execute("INSERT OR IGNORE INTO sync_state(id, last_run) VALUES (1, NULL)")
        con.commit()
    finally:
        con.close()
