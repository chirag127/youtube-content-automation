"""CommentBot — post comments on YouTube videos via Selenium element automation."""

from __future__ import annotations

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from .base import BaseAutomation

# ---------------------------------------------------------------------------
# Selector constants
# ---------------------------------------------------------------------------
SEL_COMMENT_BOX = "ytd-comments #simplebox-placeholder"
SEL_COMMENT_INPUT = "ytd-commentbox #contenteditable-root"
SEL_SUBMIT_BTN = "ytd-commentbox #submit-button button"


class CommentBot(BaseAutomation):
    """Post comments on YouTube videos.

    Requires a Chrome profile with an active YouTube login session.
    Set CHROME_PROFILE env var to your Chrome user-data-dir path.

    Warning: mass-commenting may violate YouTube ToS.
    Intended for personal/educational use only.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def comment_on_video(self, video_url: str, comment_text: str) -> bool:
        """Navigate to *video_url* and post *comment_text*.

        Returns True on success, False if the comment box was not found.
        """
        self.get(video_url)
        time.sleep(3)  # let player initialise
        return self._post_comment(comment_text)

    def comment_on_videos(
        self, video_urls: list[str], comment_text: str
    ) -> dict[str, bool]:
        """Post the same comment on each video URL.

        Returns {url: success}.
        """
        results: dict[str, bool] = {}
        for url in video_urls:
            results[url] = self.comment_on_video(url.strip(), comment_text)
        return results

    def comment_from_file(self, urls_file: str, comment_text: str) -> dict[str, bool]:
        """Read video URLs from *urls_file* (one per line) and comment on each."""
        with open(urls_file) as f:
            urls = [line.strip() for line in f if line.strip()]
        return self.comment_on_videos(urls, comment_text)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _post_comment(self, text: str) -> bool:
        try:
            # Scroll to comments section to trigger lazy-load
            self.scroll_to_bottom()
            time.sleep(1)
            # Click the placeholder to activate the input
            placeholder = self._wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_COMMENT_BOX))
            )
            placeholder.click()
            time.sleep(0.5)
            # Type comment
            input_el = self._wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_COMMENT_INPUT))
            )
            input_el.send_keys(text)
            time.sleep(0.5)
            # Submit with Ctrl+Enter
            input_el.send_keys(Keys.CONTROL, Keys.RETURN)
            time.sleep(1)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
