"""Prompt store presence checks (no invented instructions)."""

from pauli.questionanswering import prompts as P


def test_generate_system_has_citation_and_gate():
    assert "[PMCID]" in P.GENERATE_SYSTEM
    assert "[GATE:" in P.GENERATE_SYSTEM
    for cat in P.GATE_ALLOWLIST:
        assert cat in P.GENERATE_SYSTEM


def test_generate_system_formats_vocab():
    rendered = P.get_generate_system()
    assert "{vocab}" not in rendered
    assert "[GATE:suicidality|prognosis|disability|pregnancy|trauma|pem-crash]" in rendered


def test_abstain_template_slots():
    s = P.ABSTAIN_TEMPLATE.format(missing="m", term="t", doctor_q="d")
    assert "cached papers" in s


def test_doctor_prompt_has_five_parts():
    assert "500" in P.DOCTOR_SUMMARY_PROMPT
    assert "{title}" in P.DOCTOR_SUMMARY_PROMPT
