"""Unit tests for corpus DB stats (no term store — removed 2026-10-12)."""

from pauli.index.terms import get_db_stats


def test_get_db_stats_missing_db():
    st = get_db_stats(None)
    assert st == {"db_bytes": None, "papers": 0, "chunks": 0, "vectors": 0}
    st = get_db_stats("/nonexistent/pauli.db")
    assert st["db_bytes"] is None
