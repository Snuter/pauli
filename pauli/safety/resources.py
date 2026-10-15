"""Frozen gating copy (single source of truth for blur-card text).

Decided per user Q&A freeze: autonomous tasks must import these constants,
never invent wording. Gentler intro at low simplicity (10-11).
"""

from __future__ import annotations

DISCLAIMER = "Research info only, not medical advice."
CRISIS_LINE = "Crisis: call 112"

SHOW_LABEL = "Show"
SKIP_LABEL = "Skip"
WHY_LABEL = "Why am I seeing this?"

WHY_STANDARD = (
    "The AI tagged this span as sensitive. Nothing reveals without your click."
)
WHY_HIDE = (
    "Hidden-detail mode: titles only until you confirm twice. "
    "Nothing reveals without your clicks."
)


def gate_intro(category: str, simplicity: int) -> str:
    """Card headline for a gated answer. Gentler at simplicity 10-11."""
    if simplicity <= 11:
        return f"This answer may mention {category}. You choose if you read it."
    return f"This answer contains {category}."
