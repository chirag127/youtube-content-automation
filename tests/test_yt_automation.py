"""Tests for yt_automation — mock the WebDriver, no real browser needed."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from yt_automation.comments import CommentBot
from yt_automation.search import YT_SEARCH_FILTER_URL, YT_SEARCH_URL, SearchClient
from yt_automation.subscriptions import SubscriptionManager
from yt_automation.watch_later import YT_SEARCH_URL as WL_SEARCH_URL
from yt_automation.watch_later import WatchLaterManager

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.find_elements.return_value = []
    driver.find_element.side_effect = Exception("not found")
    return driver


# ---------------------------------------------------------------------------
# SearchClient
# ---------------------------------------------------------------------------


def test_search_url_no_filter():
    assert "{query}" in YT_SEARCH_URL


def test_search_url_filter():
    assert "EgIQAQ" in YT_SEARCH_FILTER_URL


def test_search_client_uses_api_when_key_set(mock_driver):
    with patch.dict("os.environ", {"YOUTUBE_API_KEY": "test-key"}):
        client = SearchClient(mock_driver)
        assert client._api_key == "test-key"


def test_search_client_no_key(mock_driver):
    with patch.dict("os.environ", {}, clear=True):
        client = SearchClient(mock_driver)
        assert client._api_key is None


def test_open_search_results_navigates(mock_driver):
    with patch.dict("os.environ", {}, clear=True):
        client = SearchClient(mock_driver)
        client.open_search_results("python tutorial")
        mock_driver.get.assert_called_once()
        called_url = mock_driver.get.call_args[0][0]
        assert (
            "python+tutorial" in called_url
            or "python%20tutorial" in called_url
            or "python" in called_url
        )


# ---------------------------------------------------------------------------
# WatchLaterManager
# ---------------------------------------------------------------------------


def test_watch_later_from_search_navigates(mock_driver):
    mock_driver.find_elements.return_value = []
    mgr = WatchLaterManager(mock_driver)
    # Should not raise even with no elements
    with patch.object(mgr._wait, "until", side_effect=Exception("timeout")):
        result = mgr.from_search("test query", max_videos=5)
    assert result == 0


def test_watch_later_search_url_format():
    url = WL_SEARCH_URL.format(query="hello world")
    assert "hello world" in url


# ---------------------------------------------------------------------------
# CommentBot
# ---------------------------------------------------------------------------


def test_comment_bot_returns_false_on_timeout(mock_driver):
    bot = CommentBot(mock_driver)
    with patch.object(bot._wait, "until", side_effect=Exception("timeout")):
        result = bot._post_comment("test comment")
    assert result is False


def test_comment_on_videos_returns_dict(mock_driver):
    bot = CommentBot(mock_driver)
    with patch.object(bot, "comment_on_video", return_value=False):
        result = bot.comment_on_videos(["https://youtube.com/watch?v=abc"], "hi")
    assert isinstance(result, dict)
    assert len(result) == 1


# ---------------------------------------------------------------------------
# SubscriptionManager
# ---------------------------------------------------------------------------


def test_list_subscriptions_returns_list(mock_driver):
    mock_driver.find_elements.return_value = []
    mgr = SubscriptionManager(mock_driver)
    with patch.object(mgr, "get"), patch.object(mgr, "scroll_to_bottom"):
        result = mgr.list_subscriptions()
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# driver module
# ---------------------------------------------------------------------------


def test_build_driver_imports():
    from yt_automation.driver import DEFAULT_WAIT, build_driver, wait

    assert DEFAULT_WAIT == 15
    assert callable(build_driver)
    assert callable(wait)
