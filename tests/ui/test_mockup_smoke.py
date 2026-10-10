"""Smoke tests for the static ui-mockup (pytest-playwright, Chromium)."""

import re


def test_onboarding_visible_by_default(page, mockup_url):
    page.goto(mockup_url)
    heading = page.get_by_role("heading", name="Set up P.A.U.L.I. in 2 steps")
    heading.wait_for()
    assert heading.is_visible()