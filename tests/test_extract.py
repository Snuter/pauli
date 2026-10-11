"""Unit tests for AI buzzword extraction (mocked chat model, no network)."""

from pauli.questionanswering.extract import (
    build_extraction_prompt,
    extract_terms,
    parse_extraction_response,
)


def test_parse_splits_lines_commas_and_dedups():
    out = parse_extraction_response("PEM\npost-exertional malaise, PEM\n- Fatigue")
    assert out == ["pem", "post-exertional malaise", "fatigue"]


def test_parse_drops_empty_and_single_char():
    assert parse_extraction_response("\n, ;\na\n  \nmyalgic encephalomyelitis") == [
        "myalgic encephalomyelitis"
    ]
    assert parse_extraction_response("") == []


def test_parse_lowercases_and_trims_numbering():
    out = parse_extraction_response("1. Myalgic Encephalomyelitis\n2) PEM Crash")
    assert out == ["myalgic encephalomyelitis", "pem crash"]


def test_build_prompt_includes_history_for_followups():
    p = build_extraction_prompt("what about treatment?", ["What triggers PEM?"])
    assert "What triggers PEM?" in p
    assert "what about treatment?" in p


def test_extract_uses_history_and_empty_question_short_circuits():
    calls = []

    def chat_fn(prompt):
        calls.append(prompt)
        return "PEM\npacing"

    assert extract_terms("crash after effort?", ["What triggers PEM?"], chat_fn) == [
        "pem",
        "pacing",
    ]
    assert "What triggers PEM?" in calls[0]
    assert extract_terms("   ", [], chat_fn) == []
    assert len(calls) == 1  # empty question never calls the model
