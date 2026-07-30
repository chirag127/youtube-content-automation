"""WatchLaterManager — add videos to Watch Later via Selenium element automation.

Watch Later is not exposed by the YouTube Data API v3, so all methods
use element-based Selenium automation (aria-labels, CSS selectors).
No pixel coordinates or image matching.
"""

from __future__ import annotations

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from .base import BaseAutomation

# ---------------------------------------------------------------------------
# Selector constants — update here when YouTube's DOM changes
# ---------------------------------------------------------------------------
SEL_VIDEO_RENDERER = "ytd-video-renderer,ytd-compact-video-renderer"
SEL_THREE_DOT_MENU = "ytd-video-renderer #button[aria-label='Action menu']"
SEL_SEARCH_THREE_DOT = "#dismissible ytd-menu-renderer yt-icon-button"
ARIA_SAVE_TO_WATCH_LATER = "Save to Watch later"
ARIA_WATCH_LATER_MENU_ITEM = "Save to Watch later"
SEL_MENU_ITEMS = "ytd-menu-service-item-renderer"
SEL_HISTORY_VIDEO = "ytd-video-renderer"
SEL_WATCH_LATER_ITEM_MENU = (
    "ytd-playlist-video-renderer ytd-menu-renderer yt-icon-button"
)

YT_SEARCH_URL = "https://www.youtube.com/results?search_query={query}"
YT_HISTORY_URL = "https://www.youtube.com/feed/history"


class WatchLaterManager(BaseAutomation):
    """Add videos to YouTube Watch Later playlist.

    Requires a Chrome profile with an active YouTube login session.
    Set CHROME_PROFILE env var to your Chrome user-data-dir path, or
    pass profile_dir to driver.build_driver().
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def from_search(self, query: str, max_videos: int = 20) -> int:
        """Search for *query* and add up to *max_videos* results to Watch Later.

        Returns the number of videos successfully added.
        """
        self.get(YT_SEARCH_URL.format(query=query))
        return self._add_visible_videos(max_videos)

    def from_search_list(
        self, queries: list[str], max_per_query: int = 20
    ) -> dict[str, int]:
        """Run from_search for each query. Returns {query: count_added}."""
        results: dict[str, int] = {}
        for q in queries:
            results[q] = self.from_search(q, max_per_query)
        return results

    def from_history(self, max_videos: int = 20) -> int:
        """Add videos from Watch History to Watch Later.

        Returns the number of videos successfully added.
        """
        self.get(YT_HISTORY_URL)
        return self._add_visible_videos(max_videos)

    def from_all_results(
        self, query: str, scroll_rounds: int = 10, max_videos: int = 100
    ) -> int:
        """Search *query*, scroll to load more results, then add all to Watch Later.

        Returns the number of videos successfully added.
        """
        self.get(YT_SEARCH_URL.format(query=query))
        for _ in range(scroll_rounds):
            self.scroll_to_bottom()
            time.sleep(1.5)
        return self._add_visible_videos(max_videos)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _add_visible_videos(self, max_videos: int) -> int:
        """Iterate visible video renderers and save each one to Watch Later."""
        added = 0
        try:
            self._wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SEL_VIDEO_RENDERER))
            )
        except TimeoutException:
            return 0

        videos = self.driver.find_elements(By.CSS_SELECTOR, SEL_VIDEO_RENDERER)
        for video in videos[:max_videos]:
            try:
                self.scroll_into_view(video)
                time.sleep(0.3)
                # Hover to make the three-dot menu appear
                menu_btn = video.find_element(
                    By.XPATH, ".//yt-icon-button[@aria-label='Action menu']"
                )
                self.driver.execute_script("arguments[0].click();", menu_btn)
                time.sleep(0.4)
                self._click_save_to_watch_later_menu_item()
                added += 1
                time.sleep(0.3)
            except (NoSuchElementException, TimeoutException):
                continue
        return added

    def _click_save_to_watch_later_menu_item(self) -> None:
        """Click the 'Save to Watch later' item in the open context menu."""
        xpath = (
            "//ytd-menu-service-item-renderer"
            f"[.//yt-formatted-string[contains(text(),'{ARIA_WATCH_LATER_MENU_ITEM}')]]"
        )
        item = self._wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        item.click()
