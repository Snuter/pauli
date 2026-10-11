"""Smoke tests for the static ui-mockup (pytest-playwright, Chromium)."""

import re


def test_setup_visible_by_default(page, mockup_url):
    page.goto(mockup_url)
    heading = page.get_by_role("heading", name="Initial Setup")
    heading.wait_for()
    assert heading.is_visible()
    assert page.locator("#view-settings").is_visible()


def test_home_reachable(page, mockup_url):
    page.goto(f"{mockup_url}#/home")
    heading = page.get_by_role("heading", name="Welcome to P.A.U.L.I.")
    heading.wait_for()
    assert heading.is_visible()
    assert page.locator("#view-home").is_visible()


def test_settings_reachable(page, mockup_url):
    page.goto(f"{mockup_url}#/settings")
    heading = page.get_by_role("heading", name="Settings")
    heading.wait_for()
    assert heading.is_visible()
    for name in ["Initial Setup", "Ollama setup", "Retrieval strictness", "Your topic", "Subscription email (optional)", "Preferences", "Sensitivity (gating)", "Simplicity of wording"]:
        assert page.get_by_role("heading", name=name).is_visible()
    # Anchor sub-routes land on the same page at the right group.
    page.goto(f"{mockup_url}#/settings/preferences")
    assert page.locator("#view-settings").is_visible()
    assert page.get_by_role("heading", name="Preferences").is_visible()
    page.goto(f"{mockup_url}#/settings/setup")
    assert page.locator("#view-settings").is_visible()
    assert page.get_by_role("heading", name="Initial Setup").is_visible()


def _select_session(page, title):
    page.locator("#session-list button", has_text=title).click()


def test_sessions_seeded(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    items = page.locator("#session-list button").all_text_contents()
    assert "ME/CFS therapies and details" in items
    assert "ME/CFS cure research" in items
    # No redundant per-view dropdowns: sidebar is the single picker.
    assert page.locator("#session-select").count() == 0
    assert page.locator("#doctor-session-select").count() == 0
    # No Ask entry in the top nav: sessions are the entry point to chat.
    assert page.get_by_role("link", name="Ask").count() == 0
    # No Doctor entry in the top nav: doctor summary lives in the Ask session buttons.
    assert page.get_by_role("link", name="Doctor").count() == 0
    # No sidebar delete button: deletion lives in the Ask buttons with confirmation.
    assert page.locator("#session-delete").count() == 0
    # Per-session buttons sit side by side below the session title.
    assert page.get_by_role("button", name="Doctor summary / print").is_visible()
    assert page.get_by_role("button", name="Delete this session").is_visible()


def test_session_opens_chat(page, mockup_url):
    page.goto(mockup_url)
    page.locator("#session-list").wait_for()
    _select_session(page, "ME/CFS cure research")
    assert page.locator("#view-ask").is_visible()
    assert "ME/CFS cure research" in page.locator("#ask-title").text_content()


def test_session_history_isolated(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    _select_session(page, "ME/CFS therapies and details")
    assert "ME/CFS therapies and details" in page.locator("#ask-title").text_content()
    page.locator("#ask-input").fill("What triggers PEM?")
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li").first.wait_for()
    assert page.locator("#history-list li").count() == 1
    _select_session(page, "ME/CFS cure research")
    assert page.locator("#history-list li").count() == 0
    assert page.locator("#history-empty").is_visible()
    _select_session(page, "ME/CFS therapies and details")
    assert page.locator("#history-list li").count() == 1


def test_doctor_sheet_per_session(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    _select_session(page, "ME/CFS therapies and details")
    page.locator("#ask-input").fill("What triggers PEM?")
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li").first.wait_for()
    # Doctor summary opens from the Ask session buttons, not the top nav.
    page.locator("#view-ask").is_visible()
    page.locator("#menu-doctor").click()
    page.locator("#doctor-dialog[open]").wait_for()
    assert "ME/CFS therapies and details" in page.locator("#sheet-session").text_content()
    assert "What triggers PEM?" in page.locator("#sheet-q").text_content()


def test_session_menu_delete_with_confirm(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    _select_session(page, "ME/CFS cure research")
    page.locator("#menu-delete").click()
    page.locator("#delete-dialog[open]").wait_for()
    assert "ME/CFS cure research" in page.locator("#delete-dialog-text").text_content()
    page.locator("#delete-confirm").click()
    items = page.locator("#session-list button").all_text_contents()
    assert "ME/CFS cure research" not in items
    assert "ME/CFS therapies and details" in items
    assert "ME/CFS therapies and details" in page.locator("#ask-title").text_content()
    # Delete the last session: heading falls back to the empty state.
    page.locator("#session-list button", has_text="ME/CFS therapies and details").click()
    page.locator("#menu-delete").click()
    page.locator("#delete-dialog[open]").wait_for()
    page.locator("#delete-confirm").click()
    assert page.locator("#session-list button").count() == 0
    # Delete the last session: home screen replaces the empty Ask state.
    assert page.locator("#view-home").is_visible()
    assert page.locator("#view-ask").is_hidden()
    assert page.locator("#ask-form").is_hidden()
