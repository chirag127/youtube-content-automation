"""PlaybackController — watch-all, next-on-dislike, auto-advance via Selenium."""

from __future__ import annotations

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from .base import BaseAutomation

# ---------------------------------------------------------------------------
# Selector constants
# ---------------------------------------------------------------------------
SEL_DISLIKE_BTN = "ytd-toggle-button-renderer:has(yt-icon[icon='dislike'])"
ARIA_DISLIKE = "Dislike this video"
ARIA_NEXT = "Next"
SEL_NEXT_BTN = ".ytp-next-button"
SEL_PLAYLIST_ITEMS = "ytd-playlist-video-renderer"
SEL_PROGRESS_BAR = ".ytp-progress-bar"
SEL_PLAYER = "#movie_player"

YT_WATCH_LATER_URL = "https://www.youtube.com/playlist?list=WL"


class PlaybackController(BaseAutomation):
    """Control YouTube video playback.

    Requires a Chrome profile with an active YouTube login session.
    Set CHROME_PROFILE env var to your Chrome user-data-dir path.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def watch_all_in_watch_later(
        self,
        seconds_per_video: int = 30,
        max_videos: int = 50,
    ) -> int:
        """Open Watch Later and advance through videos.

        Plays each video for *seconds_per_video* seconds then skips to next.
        Returns the number of videos visited.
        """
        self.get(YT_WATCH_LATER_URL)
        time.sleep(3)
        visited = 0

        items = self.driver.find_elements(By.CSS_SELECTOR, SEL_PLAYLIST_ITEMS)
        for item in items[:max_videos]:
            try:
                link = item.find_element(By.CSS_SELECTOR, "a#video-title")
                self.driver.execute_script("arguments[0].click();", link)
                time.sleep(seconds_per_video)
                visited += 1
            except (NoSuchElementException, TimeoutException):
                continue

        return visited

    def skip_on_dislike(
        self,
        poll_interval: float = 2.0,
        max_polls: int = 1800,
    ) -> None:
        """Monitor the current tab; skip to next video if dislike button is pressed.

        Polls every *poll_interval* seconds.  Stop by interrupting the process.
        """
        polls = 0
        while polls < max_polls:
            try:
                dislike = self.driver.find_element(
                    By.XPATH, f"//*[@aria-label='{ARIA_DISLIKE}']"
                )
                if dislike.get_attribute("aria-pressed") == "true":
                    self._press_next()
                    time.sleep(1)
            except NoSuchElementException:
                pass
            time.sleep(poll_interval)
            polls += 1

    def auto_advance(
        self,
        pause: bool = False,
        advance_interval: float = 3.0,
        max_advances: int = 200,
    ) -> None:
        """Press the End key + advance through playlist items.

        Set *pause* to True to stop advancing (blocks until set back to False).
        Stop by interrupting the process.
        """
        for _ in range(max_advances):
            if not pause:
                self._press_next()
                time.sleep(advance_interval)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _press_next(self) -> None:
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, SEL_NEXT_BTN)
            btn.click()
        except NoSuchElementException:
            player = self.driver.find_element(By.CSS_SELECTOR, SEL_PLAYER)
            player.send_keys(Keys.SHIFT + "n")
