"""Corpus stats helper (transient terms — no persisted term store).

Removed 2026-10-12: `TermStore` deleted per spec (terms are transient per
Ask, ID-first PMCID-dedup against a growing DB). Only `get_db_stats()`
remains for Settings DB stats.
"""

from __future__ import annotations

import sqlite3


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
