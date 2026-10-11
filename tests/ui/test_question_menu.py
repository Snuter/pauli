"""Tests for per-question menu: move up/down, edit & rerun, delete."""

import uuid


def _fresh_session(page, mockup_url, title):
    page.goto(mockup_url)
    page.evaluate("localStorage.clear()")
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()
    page.locator("#session-new").fill(title)
    page.locator("#session-add").click()
    assert title in page.locator("#ask-title").text_content()


def _ask(page, text):
    page.locator("#ask-input").fill(text)
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li", has_text=text).first.wait_for()


def _questions(page):
    return page.locator("#history-list li .q").all_text_contents()


def test_question_menu_visible_and_bounds(page, mockup_url):
    title = f"menu-bounds-{uuid.uuid4().hex[:6]}"
    _fresh_session(page, mockup_url, title)
    _ask(page, "What triggers PEM?")
    _ask(page, "Is there a cure?")
    items = page.locator("#history-list li")
    assert items.count() == 2
    # Icon row visible on each question.
    for i in range(2):
        row = items.nth(i).locator(".q-actions")
        assert row.is_visible()
        assert row.get_by_role("button", name="Move question up").count() == 1
        assert row.get_by_role("button", name="Move question down").count() == 1
        assert row.get_by_role("button", name="Edit question and rerun answer").count() == 1
        assert row.get_by_role("button", name="Delete question").count() == 1
    # Bounds: first up disabled, last down disabled.
    assert items.nth(0).get_by_role("button", name="Move question up").is_disabled()
    assert not items.nth(0).get_by_role("button", name="Move question down").is_disabled()
    assert items.nth(1).get_by_role("button", name="Move question down").is_disabled()
    assert not items.nth(1).get_by_role("button", name="Move question up").is_disabled()


def test_move_question_up_down_and_persist(page, mockup_url):
    title = f"menu-move-{uuid.uuid4().hex[:6]}"
    _fresh_session(page, mockup_url, title)
    _ask(page, "What triggers PEM?")
    _ask(page, "Is there a cure?")
    assert _questions(page) == ["What triggers PEM?", "Is there a cure?"]
    # Move second up.
    page.locator("#history-list li").nth(1).get_by_role("button", name="Move question up").click()
    assert _questions(page) == ["Is there a cure?", "What triggers PEM?"]
    # Doctor sheet follows new first question.
    page.locator("#menu-doctor").click()
    page.locator("#doctor-dialog[open]").wait_for()
    assert "Is there a cure?" in page.locator("#sheet-q").text_content()
    page.locator("#doctor-close").click()
    # Move first back down.
    page.locator("#history-list li").nth(0).get_by_role("button", name="Move question down").click()
    assert _questions(page) == ["What triggers PEM?", "Is there a cure?"]
    # Order survives reload.
    page.reload()
    page.locator("#session-list").wait_for()
    assert _questions(page) == ["What triggers PEM?", "Is there a cure?"]


def test_edit_question_reruns_answer_in_place(page, mockup_url):
    title = f"menu-edit-{uuid.uuid4().hex[:6]}"
    _fresh_session(page, mockup_url, title)
    _ask(page, "What is xyzzy unknown thing?")
    _ask(page, "What triggers PEM?")
    assert _questions(page) == ["What is xyzzy unknown thing?", "What triggers PEM?"]
    page.locator("#history-list li").nth(0).get_by_role("button", name="Edit question and rerun answer").click()
    page.locator("#qedit-dialog[open]").wait_for()
    assert page.locator("#qedit-input").input_value() == "What is xyzzy unknown thing?"
    page.locator("#qedit-input").fill("Is there a cure?")
    page.locator("#qedit-confirm").click()
    # Replaced in place: same position, new Q + fresh (cure) answer.
    assert _questions(page) == ["Is there a cure?", "What triggers PEM?"]
    first = page.locator("#history-list li").nth(0)
    assert "PMC1111111" in first.text_content()
    page.reload()
    page.locator("#session-list").wait_for()
    assert _questions(page) == ["Is there a cure?", "What triggers PEM?"]


def test_edit_empty_rejected(page, mockup_url):
    title = f"menu-edit-empty-{uuid.uuid4().hex[:6]}"
    _fresh_session(page, mockup_url, title)
    _ask(page, "What triggers PEM?")
    page.locator("#history-list li").nth(0).get_by_role("button", name="Edit question and rerun answer").click()
    page.locator("#qedit-dialog[open]").wait_for()
    page.locator("#qedit-input").fill("   ")
    page.locator("#qedit-confirm").click()
    # Dialog stays open with hint; question unchanged.
    assert page.locator("#qedit-dialog[open]").count() == 1
    assert "Empty question" in page.locator("#qedit-hint").text_content()
    page.locator("#qedit-cancel").click()
    assert _questions(page) == ["What triggers PEM?"]


def test_delete_question_with_confirm_and_cancel(page, mockup_url):
    title = f"menu-del-{uuid.uuid4().hex[:6]}"
    _fresh_session(page, mockup_url, title)
    _ask(page, "What triggers PEM?")
    _ask(page, "Is there a cure?")
    # Cancel path keeps both.
    page.locator("#history-list li").nth(0).get_by_role("button", name="Delete question").click()
    page.locator("#qdelete-dialog[open]").wait_for()
    assert "What triggers PEM?" in page.locator("#qdelete-dialog-text").text_content()
    page.locator("#qdelete-cancel").click()
    assert page.locator("#history-list li").count() == 2
    # Confirm path removes in-session only.
    page.locator("#history-list li").nth(0).get_by_role("button", name="Delete question").click()
    page.locator("#qdelete-dialog[open]").wait_for()
    page.locator("#qdelete-confirm").click()
    assert _questions(page) == ["Is there a cure?"]
    assert page.locator("#history-empty").is_hidden()
    page.reload()
    page.locator("#session-list").wait_for()
    assert _questions(page) == ["Is there a cure?"]
