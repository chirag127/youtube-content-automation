"""SearchClient — search YouTube via the Data API v3 and/or Selenium."""

from __future__ import annotations

import os
import time
import urllib.parse

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base import BaseAutomation

# ---------------------------------------------------------------------------
# Selector constants
# ---------------------------------------------------------------------------
SEL_SEARCH_BOX = "input#search"
SEL_SEARCH_BTN = "button#search-icon-legacy"
SEL_VIDEO_TITLE = "ytd-video-renderer #video-title"

YT_SEARCH_URL = "https://www.youtube.com/results?search_query={query}"
YT_SEARCH_FILTER_URL = (
    "https://www.youtube.com/results?search_query={query}&sp=EgIQAQ%253D%253D"
)

# YouTube Data API v3 search endpoint
YT_API_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


class SearchClient(BaseAutomation):
    """Search YouTube using the Data API v3 (preferred) or Selenium fallback.

    For API-based search, set the YOUTUBE_API_KEY environment variable.
    Selenium fallback works without an API key but requires a browser.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        super().__init__(driver, timeout)
        self._api_key: str | None = os.environ.get("YOUTUBE_API_KEY")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(self, query: str, max_results: int = 10) -> list[dict]:
        """Search YouTube for *query*.

        Uses the Data API v3 when YOUTUBE_API_KEY is set; falls back to
        Selenium element scraping otherwise.

        Returns list of dicts with at least: title, url, video_id.
        """
        if self._api_key:
            return self._api_search(query, max_results)
        return self._selenium_search(query, max_results)

    def search_topics(
        self, topics: list[str], max_per_topic: int = 10
    ) -> dict[str, list[dict]]:
        """Search each topic and return combined results keyed by topic."""
        return {topic: self.search(topic, max_per_topic) for topic in topics}

    def open_search_results(self, query: str, filter_videos: bool = True) -> None:
        """Open the YouTube search results page for *query* in the browser."""
        url_template = YT_SEARCH_FILTER_URL if filter_videos else YT_SEARCH_URL
        self.get(url_template.format(query=urllib.parse.quote_plus(query)))

    def open_all_topics(self, topics: list[str]) -> None:
        """Open a search results tab for each topic (browser tabs)."""
        for topic in topics:
            self.driver.execute_script(
                f"window.open('{YT_SEARCH_URL.format(query=urllib.parse.quote_plus(topic))}');"
            )
            time.sleep(0.3)

    # ------------------------------------------------------------------
    # API-based search
    # ------------------------------------------------------------------

    def _api_search(self, query: str, max_results: int) -> list[dict]:
        import json
        import urllib.request

        params = urllib.parse.urlencode(
            {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": min(max_results, 50),
                "key": self._api_key,
            }
        )
        url = f"{YT_API_SEARCH_URL}?{params}"
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())

        results = []
        for item in data.get("items", []):
            vid_id = item["id"].get("videoId", "")
            snippet = item.get("snippet", {})
            results.append(
                {
                    "video_id": vid_id,
                    "title": snippet.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "channel": snippet.get("channelTitle", ""),
                    "description": snippet.get("description", ""),
                }
            )
        return results

    # ------------------------------------------------------------------
    # Selenium fallback
    # ------------------------------------------------------------------

    def _selenium_search(self, query: str, max_results: int) -> list[dict]:
        self.open_search_results(query, filter_videos=False)
        try:
            self._wait.until(
                lambda d: d.find_elements(By.CSS_SELECTOR, SEL_VIDEO_TITLE)
            )
        except TimeoutException:
            return []

        items = self.driver.find_elements(By.CSS_SELECTOR, SEL_VIDEO_TITLE)
        results = []
        for el in items[:max_results]:
            try:
                href = el.get_attribute("href") or ""
                results.append(
                    {
                        "title": el.text.strip(),
                        "url": href,
                        "video_id": href.split("v=")[-1].split("&")[0]
                        if "v=" in href
                        else "",
                    }
                )
            except NoSuchElementException:
                continue
        return results
