"""Unit tests for the auto-collected term store (scheduled-cap LRU, no DB)."""

from pauli.index.terms import TermStore, get_db_stats


def test_add_dedups_and_normalizes():
    s = TermStore(max_terms=500)
    added = s.add_many(["PEM", " pem ", "Post-Exertional Malaise", "x", ""])
    assert added == ["pem", "post-exertional malaise"]
    assert len(s) == 2


def test_over_cap_defers_eviction_until_prune():
    s = TermStore(max_terms=3)
    s.add_many(["a1", "b2", "c3"])
    s.touch("a1")  # a1 most recent, b2 oldest
    s.add_many(["d4"])
    assert s.over_limit is True
    assert len(s) == 4  # no immediate eviction: scheduled cap only
    pruned = s.prune_now(now=1000.0)
    assert pruned == ["b2"]
    terms = [d["term"] for d in s.list_terms()]
    assert set(terms) == {"a1", "c3", "d4"}


def test_prune_due_respects_cadence():
    s = TermStore(max_terms=2, prune_freq="daily", last_prune=0.0)
    s.add_many(["a1", "b2", "c3"])
    assert s.prune_due(now=10.0) is False  # window not elapsed
    assert s.maybe_prune(now=10.0) == []
    assert len(s) == 3
    pruned = s.maybe_prune(now=90_000.0)
    assert len(pruned) == 1
    assert len(s) == 2


def test_remove_and_set_limit_defers_prune():
    s = TermStore(max_terms=500)
    s.add_many(["pem", "pacing", "fatigue"])
    assert s.remove("PEM") is True
    assert s.remove("missing") is False
    s.set_limit(2)
    assert len(s) == 2  # already at limit: nothing deferred
    s.set_limit(1)
    assert len(s) == 2  # over limit but not pruned yet
    assert s.over_limit is True
    s.prune_now(now=5.0)
    assert len(s) == 1


def test_mark_complete_and_order_newest_first():
    s = TermStore(max_terms=500)
    s.add_many(["pem"])
    s.add_many(["pacing"])
    s.mark_complete("pem", paper_count=42)
    by_term = {d["term"]: d for d in s.list_terms()}
    assert by_term["pem"]["status"] == "complete"
    assert by_term["pem"]["paper_count"] == 42
    assert s.list_terms()[0]["term"] == "pacing"


def test_stats_counts_for_limit_picker():
    s = TermStore(max_terms=2)
    s.add_many(["pem", "pacing"])
    s.mark_complete("pem", paper_count=42)
    st = s.stats()
    assert st["total_terms"] == 2
    assert st["digesting"] == 1
    assert st["complete"] == 1
    assert st["total_papers"] == 42
    assert st["avg_papers"] == 21.0
    assert st["over_limit"] is False


def test_get_db_stats_missing_db():
    st = get_db_stats(None)
    assert st == {"db_bytes": None, "papers": 0, "chunks": 0, "vectors": 0}
    st = get_db_stats("/nonexistent/pauli.db")
    assert st["db_bytes"] is None
