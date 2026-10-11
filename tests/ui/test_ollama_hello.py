"""Ollama 'Test Ollama' button (pytest-playwright, Chromium)."""

import re

from playwright.sync_api import expect


def test_hello_shows_model_greeting(page, mockup_url):
    page.goto(mockup_url)
    page.locator("#ollama-chat").fill("test-model")
    page.route(
        re.compile(r".*/api/chat"),
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"message": {"content": "Hi there!"}}',
        ),
    )
    page.get_by_role("button", name="Test Ollama", exact=True).click()
    status = page.locator("#ollama-hello-status")
    expect(status).to_contain_text("Hi there!")


def test_hello_missing_model_fails_closed(page, mockup_url):
    page.goto(mockup_url)
    page.locator("#ollama-chat").fill("")
    page.get_by_role("button", name="Test Ollama", exact=True).click()
    expect(page.locator("#ollama-hello-status")).to_contain_text("No chat model configured")


def test_hello_unreachable_host_shows_error(page, mockup_url):
    page.goto(mockup_url)
    page.locator("#ollama-chat").fill("test-model")
    page.route(re.compile(r".*/api/chat"), lambda route: route.abort())
    page.get_by_role("button", name="Test Ollama", exact=True).click()
    status = page.locator("#ollama-hello-status")
    expect(status).not_to_contain_text("Hi there!")
    assert status.text_content() != ""
