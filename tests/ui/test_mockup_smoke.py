"""Smoke tests for the static ui-mockup (pytest-playwright, Chromium)."""

import re


def test_onboarding_visible_by_default(page, mockup_url):
    page.goto(mockup_url)
    heading = page.get_by_role("heading", name="Set up P.A.U.L.I. in 2 steps")
    heading.wait_for()
    assert heading.is_visible()


def test_sessions_seeded(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    sel = page.locator("#session-select")
    sel.wait_for()
    options = sel.locator("option").all_text_contents()
    assert "ME/CFS therapies and details" in options
    assert "ME/CFS cure research" in options


def test_session_history_isolated(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-select").wait_for()
    page.locator("#session-select").select_option(label="ME/CFS therapies and details")
    page.locator("#ask-input").fill("What triggers PEM?")
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li").first.wait_for()
    assert page.locator("#history-list li").count() == 1
    page.locator("#session-select").select_option(label="ME/CFS cure research")
    assert page.locator("#history-list li").count() == 0
    assert page.locator("#history-empty").is_visible()
    page.locator("#session-select").select_option(label="ME/CFS therapies and details")
    assert page.locator("#history-list li").count() == 1


def test_doctor_sheet_per_session(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-select").wait_for()
    page.locator("#session-select").select_option(label="ME/CFS therapies and details")
    page.locator("#ask-input").fill("What triggers PEM?")
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li").first.wait_for()
    page.goto(f"{mockup_url}#/doctor")
    page.locator("#doctor-session-select").wait_for()
    page.locator("#doctor-session-select").select_option(label="ME/CFS therapies and details")
    assert "ME/CFS therapies and details" in page.locator("#sheet-session").text_content()
    assert "What triggers PEM?" in page.locator("#sheet-q").text_content()