"""Auto-collected term store for the single shared corpus.

Scheduled-cap LRU: ``max_terms`` (default 500, user-configurable in Settings)
is enforced only on the auto-prune schedule (``prune_freq`` daily/weekly/
monthly, default daily). ``add_many``/``set_limit`` never evict immediately;
callers run ``maybe_prune``/``prune_now`` on schedule and then delete the
pruned terms' vectors.
"""

from __future__ import annotations

import sqlite3
import time
from collections.abc import Iterable

PRUNE_FREQS = ("daily", "weekly", "monthly")
_PRUNE_WINDOW_S = {"daily": 86_400, "weekly": 7 * 86_400, "monthly": 30 * 86_400}


class TermStore:
    def __init__(
        self,
        max_terms: int = 500,
        prune_freq: str = "daily",
        last_prune: float | None = None,
    ) -> None:
        self.max_terms = max(1, max_terms)
        self.prune_freq = prune_freq if prune_freq in PRUNE_FREQS else "daily"
        self.last_prune = last_prune
        self._terms: dict[str, dict] = {}
        self._tick = 0

    def _norm(self, term: str) -> str:
        return " ".join(term.strip().lower().split())

    def _touch_new(self, term: str) -> None:
        self._tick += 1
        self._terms[term]["last_used"] = self._tick

    def add_many(self, terms: Iterable[str]) -> list[str]:
        """Add terms (dedup, skip empties). Returns newly added terms."""
        added: list[str] = []
        for raw in terms:
            term = self._norm(raw)
            if len(term) < 2:
                continue
            if term in self._terms:
                self._touch_new(term)
                continue
            self._tick += 1
            self._terms[term] = {
                "first_seen": self._tick,
                "last_used": self._tick,
                "paper_count": 0,
                "status": "digesting",
            }
            added.append(term)
        return added

    def _evict(self) -> list[str]:
        pruned: list[str] = []
        while len(self._terms) > self.max_terms:
            oldest = min(self._terms, key=lambda k: self._terms[k]["last_used"])
            pruned.append(oldest)
            del self._terms[oldest]
        return pruned

    @property
    def over_limit(self) -> bool:
        return len(self._terms) > self.max_terms

    def prune_now(self, now: float | None = None) -> list[str]:
        """Enforce the cap now (LRU). Returns pruned term names."""
        pruned = self._evict()
        self.last_prune = now if now is not None else time.time()
        return pruned

    def prune_due(self, now: float | None = None) -> bool:
        """True when over the cap and the schedule window has elapsed."""
        if not self.over_limit:
            return False
        if self.last_prune is None:
            return True
        now = now if now is not None else time.time()
        return (now - self.last_prune) >= _PRUNE_WINDOW_S[self.prune_freq]

    def maybe_prune(self, now: float | None = None) -> list[str]:
        """Prune only when due; otherwise no-op. Returns pruned terms."""
        if not self.prune_due(now):
            return []
        return self.prune_now(now)

    def set_prune_freq(self, freq: str) -> None:
        if freq in PRUNE_FREQS:
            self.prune_freq = freq

    def touch(self, term: str) -> None:
        term = self._norm(term)
        if term in self._terms:
            self._touch_new(term)

    def remove(self, term: str) -> bool:
        return self._terms.pop(self._norm(term), None) is not None

    def mark_complete(self, term: str, paper_count: int = 0) -> None:
        term = self._norm(term)
        if term in self._terms:
            self._terms[term]["status"] = "complete"
            self._terms[term]["paper_count"] = paper_count

    def set_limit(self, n: int) -> None:
        self.max_terms = max(1, n)

    def stats(self) -> dict:
        """Counts to help pick a term limit (no per-term dump)."""
        total = len(self._terms)
        digesting = sum(1 for v in self._terms.values() if v.get("status") != "complete")
        complete = total - digesting
        total_papers = sum(int(v.get("paper_count", 0) or 0) for v in self._terms.values())
        return {
            "total_terms": total,
            "max_terms": self.max_terms,
            "over_limit": total > self.max_terms,
            "over_by": max(0, total - self.max_terms),
            "digesting": digesting,
            "complete": complete,
            "total_papers": total_papers,
            "avg_papers": (total_papers / total) if total else 0.0,
            "prune_freq": self.prune_freq,
        }

    def list_terms(self) -> list[dict]:
        return sorted(
            ({"term": k, **v} for k, v in self._terms.items()),
            key=lambda d: d["last_used"],
            reverse=True,
        )

    def __len__(self) -> int:
        return len(self._terms)


def get_db_stats(db_path: str | None = None) -> dict:
    """Best-effort DB stats for the limit picker; zeros when no DB yet."""
    stats: dict = {"db_bytes": None, "papers": 0, "chunks": 0, "vectors": 0}
    if not db_path:
        return stats
    try:
        import os as _os

        stats["db_bytes"] = _os.path.getsize(db_path)
    except OSError:
        return stats
    try:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            for key, table in (("papers", "papers"), ("chunks", "chunks")):
                try:
                    stats[key] = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                except sqlite3.Error:
                    pass
            stats["vectors"] = stats["chunks"]
        finally:
            con.close()
    except sqlite3.Error:
        pass
    return stats
