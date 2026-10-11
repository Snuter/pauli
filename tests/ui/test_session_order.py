"""Research sessions are ordered newest-first by creation timestamp."""

import uuid


def _sidebar_titles(page):
    return page.locator("#session-list button").all_text_contents()


def test_sessions_newest_first_rename_moves_to_top(page, mockup_url):
    page.goto(mockup_url)
    page.evaluate("localStorage.clear()")
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()

    suffix = uuid.uuid4().hex[:6]
    first = f"order-first-{suffix}"
    second = f"order-second-{suffix}"

    page.locator("#session-new").fill(first)
    page.locator("#session-add").click()
    assert first in page.locator("#ask-title").text_content()
    page.locator("#session-new").fill(second)
    page.locator("#session-add").click()
    assert second in page.locator("#ask-title").text_content()

    titles = _sidebar_titles(page)
    assert titles.index(second) < titles.index(first)

    renamed = f"{first}-renamed"
    page.locator("#session-list button", has_text=first).click()
    page.locator("#menu-rename").click()
    page.locator("#rename-dialog[open]").wait_for()
    page.locator("#rename-input").fill(renamed)
    page.locator("#rename-confirm").click()
    titles = _sidebar_titles(page)
    assert titles.index(renamed) < titles.index(second)

    page.reload()
    page.locator("#session-list").wait_for()
    titles = _sidebar_titles(page)
    assert titles.index(renamed) < titles.index(second)


def _ask(page, text):
    page.locator("#ask-input").fill(text)
    page.locator("#ask-form button[type=submit]").click()
    page.locator("#history-list li", has_text=text).first.wait_for()


def test_session_bumps_to_top_on_ask_and_edit(page, mockup_url):
    page.goto(mockup_url)
    page.evaluate("localStorage.clear()")
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()

    suffix = uuid.uuid4().hex[:6]
    first = f"bump-first-{suffix}"
    second = f"bump-second-{suffix}"

    page.locator("#session-new").fill(first)
    page.locator("#session-add").click()
    page.locator("#session-new").fill(second)
    page.locator("#session-add").click()
    assert _sidebar_titles(page).index(second) < _sidebar_titles(page).index(first)

    # Asking in the older session bumps it to the top.
    page.locator("#session-list button", has_text=first).click()
    _ask(page, "What triggers PEM?")
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)

    # Asking in the other session bumps it back to the top.
    page.locator("#session-list button", has_text=second).click()
    _ask(page, "What triggers PEM?")
    assert _sidebar_titles(page).index(second) < _sidebar_titles(page).index(first)

    # Editing a question bumps its session to the top.
    page.locator("#session-list button", has_text=first).click()
    page.locator("#history-list li").nth(0).get_by_role("button", name="Edit question and rerun answer").click()
    page.locator("#qedit-dialog[open]").wait_for()
    page.locator("#qedit-input").fill("Is there a cure?")
    page.locator("#qedit-confirm").click()
    page.locator("#history-list li", has_text="Is there a cure?").first.wait_for()
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)

    page.reload()
    page.locator("#session-list").wait_for()
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)


def test_session_bumps_to_top_on_move_delete_and_subscribe(page, mockup_url):
    page.goto(mockup_url)
    page.evaluate("localStorage.clear()")
    page.goto(f"{mockup_url}#/ask")
    page.locator("#session-list").wait_for()

    suffix = uuid.uuid4().hex[:6]
    first = f"activity-first-{suffix}"
    second = f"activity-second-{suffix}"

    page.locator("#session-new").fill(first)
    page.locator("#session-add").click()
    page.locator("#session-new").fill(second)
    page.locator("#session-add").click()
    assert _sidebar_titles(page).index(second) < _sidebar_titles(page).index(first)

    # Two questions in the older session so one can be moved.
    page.locator("#session-list button", has_text=first).click()
    _ask(page, "What triggers PEM?")
    _ask(page, "Is there a cure?")
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)

    # Asking in the other session bumps it back to the top.
    page.locator("#session-list button", has_text=second).click()
    _ask(page, "What triggers PEM?")
    assert _sidebar_titles(page).index(second) < _sidebar_titles(page).index(first)

    # Moving a question bumps its session to the top.
    page.locator("#session-list button", has_text=first).click()
    page.locator("#history-list li").nth(1).get_by_role("button", name="Move question up").click()
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)

    # Deleting a question bumps its session to the top.
    page.locator("#session-list button", has_text=second).click()
    page.locator("#history-list li").nth(0).get_by_role("button", name="Delete question").click()
    page.locator("#qdelete-dialog[open]").wait_for()
    page.locator("#qdelete-confirm").click()
    assert _sidebar_titles(page).index(second) < _sidebar_titles(page).index(first)

    # Toggling the subscription bumps its session to the top.
    page.locator("#session-list button", has_text=first).click()
    page.locator("#menu-sub").click()
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)

    page.reload()
    page.locator("#session-list").wait_for()
    assert _sidebar_titles(page).index(first) < _sidebar_titles(page).index(second)
