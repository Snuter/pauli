"""AI buzzword extraction from questions (+ session history).

No HTTP inside: the caller injects ``chat_fn(prompt) -> str`` (Ollama chat
model in production, stub in tests). No hit-count validation here by design:
whatever the model returns (after normalization) is accepted.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence


def build_extraction_prompt(question: str, history: Sequence[str] = ()) -> str:
    hist = "\n".join(f"- {h}" for h in history[-5:] if h and h.strip())
    ctx = f"Session history:\n{hist}\n" if hist else ""
    return (
        "Extract 1-5 short literature search terms (diseases, symptoms, "
        "mechanisms) from the patient question below. "
        f"Use session history for follow-ups.\n{ctx}"
        f"Question: {question.strip()}\n"
        "Return one term per line, no numbering, no quotes."
    )


def parse_extraction_response(text: str) -> list[str]:
    """Normalize raw LLM output: split lines/commas, strip, lowercase, dedup."""
    if not text:
        return []
    chunked: list[str] = []
    for line in text.replace(";", "\n").splitlines():
        chunked.extend(line.split(","))
    seen: set[str] = set()
    out: list[str] = []
    for raw in chunked:
        term = " ".join(raw.strip().lower().split())
        term = term.lstrip("-*0123456789. ").strip("\"'()[]{}")
        term = " ".join(term.split())
        if len(term) < 2 or term in seen:
            continue
        seen.add(term)
        out.append(term)
    return out


def extract_terms(
    question: str,
    history: Sequence[str] = (),
    chat_fn: Callable[[str], str] | None = None,
) -> list[str]:
    """Build prompt, call chat model, parse terms. Empty question -> []."""
    if not question or not question.strip():
        return []
    if chat_fn is None:
        return []
    return parse_extraction_response(chat_fn(build_extraction_prompt(question, history)))
