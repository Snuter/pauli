"""Canonical LLM prompt texts (single source of truth).

All prompts are constants here so tests can assert on wording and the
autonomous builder never invents instructions. Callers format with
``str.format``; no secrets are interpolated into prompts.
"""

from __future__ import annotations

GATE_ALLOWLIST = (
    "suicidality",
    "prognosis",
    "disability",
    "pregnancy",
    "trauma",
    "pem-crash",
)
GATE_VOCAB = "|".join(GATE_ALLOWLIST)

REWRITE_PROMPT = """Rewrite the patient question as one concise literature query for retrieval.
Use session history only for follow-up context. Do not answer, do not add facts.
Question: {question}
History:
{history}
Return one line, no quotes."""

GENERATE_SYSTEM = """You answer ONLY from the provided cached-paper chunks. No general knowledge.
Every factual sentence must end with a citation marker [PMCID] taken from the chunks.
If a claim has no supporting chunk, omit it or abstain.
At sensitive spans emit an inline tag [GATE:{vocab}] (allowed: suicidality, prognosis, disability, pregnancy, trauma, pem-crash). Never use other tag names. Missing tags mean no gate.
Keep the answer under 150 words. Plain patient language.
Research info only, not medical advice."""


def get_generate_system() -> str:
    """Render GENERATE_SYSTEM with the frozen gate vocabulary.

    Call sites MUST use this (never hand-format) so `{vocab}` never leaks
    into a model prompt. See `tests/test_prompts.py`.
    """
    return GENERATE_SYSTEM.format(vocab=GATE_VOCAB)

ABSTAIN_TEMPLATE = (
    "I don't know from your cached papers — "
    "[what is missing: {missing}; what term to add: {term}; "
    "what to ask your doctor: {doctor_q}]"
)

# LLM-labeled conflict marker: generator emits this literal line when retrieved
# chunks disagree; `abstain.should_abstain` treats its presence as the
# `conflicting` branch (code never heuristically detects contradiction).
CONFLICT_MARKER = "[CONFLICT]"

DOCTOR_SUMMARY_PROMPT = """Condense ALL Q&As of this session into one Muchas gracias printout, max ~500 words, exactly 5 parts:
1. Short answer 2. Citations ([PMCID] from retrieval set only)
3. Unknowns 4. Suggested doctor questions 5. Digest line (N new paper(s)).
Truncate with ellipsis if over 500 words; never drop citations.
Session title: {title}
Q&As:
{qas}"""

OLLAMA_HELLO_PROMPT = "Say hi briefly."
