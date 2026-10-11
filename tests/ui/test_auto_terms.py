"""Auto-collected topics: no manual input, extraction on Ask, manual refresh."""

import re


def _select_session(page, title):
    page.locator("#session-list button", has_text=title).click()


def test_no_manual_buzzword_form(page, mockup_url):
    page.goto(f"{mockup_url}#/settings")
    page.get_by_role("heading", name=re.compile("Auto-collected topics")).wait_for()
    assert page.locator("#buzz-form").count() == 0
    assert page.locator("#buzz-input").count() == 0
    assert page.locator("#buzz-fetch").count() == 0
    # Count + stats only: no per-term list.
    assert page.locator("#buzz-list").count() == 0
    assert page.locator("#terms-count").is_visible()
    assert page.locator("#terms-stats").is_visible()
    assert "auto-collected term" in (page.locator("#terms-count").text_content() or "")
    assert page.locator("#terms-limit").is_visible()
    assert page.locator("#terms-limit").input_value() == "500"
    assert page.locator("#prune-freq").is_visible()
    assert page.locator("#prune-freq").input_value() == "daily"


def test_ask_extracts_terms_and_refresh_replaces_in_place(page, mockup_url):
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    page.evaluate("localStorage.clear()")
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    _select_session(page, "ME/CFS therapies and details")
    page.locator("#ask-input").fill("What triggers postexertional malaise?")
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li").first.wait_for()
    # Incomplete badge + digest progress + manual refresh, no auto-rewrite.
    assert page.get_by_test_id("incomplete-badge").count() == 1
    assert "disclaimer" in (page.get_by_test_id("incomplete-badge").get_attribute("class") or "")
    assert page.get_by_test_id("digest-progress").count() == 1
    progress_text = page.get_by_test_id("digest-progress").text_content()
    assert progress_text.count("Digesting") == 1
    assert page.get_by_test_id("refresh-answer").count() == 1
    assert page.locator("#history-list li").count() == 1
    before = page.locator("#history-list li .a").first.text_content()
    # New term bumps the count/stats summary (no per-term list).
    page.goto(f"{mockup_url}#/settings")
    page.locator("#terms-count").wait_for()
    count_text = page.locator("#terms-count").text_content() or ""
    stats_text = (page.locator("#terms-stats").text_content() or "") + (
        page.locator("#buzz-progress").text_content() or ""
    )
    assert "auto-collected term" in count_text
    assert "Digesting" in stats_text or "digesting" in stats_text
    # Back to Ask: manual refresh replaces the same entry in place.
    page.goto(f"{mockup_url}#/ask")
    page.locator("#history-list li").first.wait_for()
    page.get_by_test_id("refresh-answer").click()
    assert page.locator("#history-list li").count() == 1
    assert page.get_by_test_id("incomplete-badge").count() == 0
    assert page.get_by_test_id("refresh-answer").count() == 0
    after = page.locator("#history-list li .a").first.text_content()
    assert after == before or "PEM" in after or "cached papers" in after
