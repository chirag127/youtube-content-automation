"""ReportManager — report YouTube videos/comments via Selenium element automation.

The YouTube Data API v3 does not expose a report endpoint, so all
reporting goes through the browser UI using element selectors.
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
# Selector constants
# ---------------------------------------------------------------------------
# Three-dot menu on a video card (search results)
SEL_VIDEO_MORE_BTN = "ytd-video-renderer ytd-menu-renderer yt-icon-button"
# Three-dot menu on the video player page
SEL_PLAYER_MORE_BTN = "ytd-menu-renderer.style-scope.ytd-watch-metadata yt-icon-button"
ARIA_MORE_ACTIONS = "More actions"

# Menu item text for reporting
REPORT_MENU_ITEM_TEXT = "Report"
# Report dialog option texts
REPORT_SPAM_TEXT = "Spam or misleading"
REPORT_SEXUAL_TEXT = "Sexual content"
REPORT_VIOLENT_TEXT = "Violent or repulsive content"
REPORT_HATEFUL_TEXT = "Hateful or abusive content"
REPORT_HARMFUL_TEXT = "Harmful or dangerous acts"
REPORT_MISINFORMATION_TEXT = "Misinformation"
REPORT_CHILD_ABUSE_TEXT = "Child abuse"

# Dialog submit button
SEL_REPORT_SUBMIT = "yt-button-renderer.style-primary button"


class ReportManager(BaseAutomation):
    """Report YouTube videos for policy violations.

    Requires a Chrome profile with an active YouTube login session.
    Set CHROME_PROFILE env var to your Chrome user-data-dir path.

    Warning: abusing the report function may violate YouTube ToS.
    Intended for legitimate personal/educational use only.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def report_video(
        self,
        video_url: str,
        reason: str = REPORT_SPAM_TEXT,
    ) -> bool:
        """Navigate to *video_url* and report it with *reason*.

        *reason* should be one of the REPORT_*_TEXT constants.
        Returns True on success.
        """
        self.get(video_url)
        time.sleep(3)
        return self._do_report(reason)

    def report_videos(
        self,
        video_urls: list[str],
        reason: str = REPORT_SPAM_TEXT,
    ) -> dict[str, bool]:
        """Report multiple videos. Returns {url: success}."""
        results: dict[str, bool] = {}
        for url in video_urls:
            results[url] = self.report_video(url.strip(), reason)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _do_report(self, reason: str) -> bool:
        try:
            # Open the three-dot / More actions menu on the player page
            more_btn = self._wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//ytd-menu-renderer[contains(@class,'ytd-watch-metadata')]"
                        f"//yt-icon-button[@aria-label='{ARIA_MORE_ACTIONS}']",
                    )
                )
            )
            more_btn.click()
            time.sleep(0.5)

            # Click "Report" menu item
            report_item = self._wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//ytd-menu-service-item-renderer"
                        f"[.//yt-formatted-string[contains(text(),'{REPORT_MENU_ITEM_TEXT}')]]",
                    )
                )
            )
            report_item.click()
            time.sleep(0.6)

            # Select the reason radio button
            reason_option = self._wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//tp-yt-paper-radio-button[@aria-label='{reason}']"
                        f" | //ytd-report-form-modal-renderer"
                        f"  //*[contains(text(),'{reason}')]",
                    )
                )
            )
            reason_option.click()
            time.sleep(0.3)

            # Submit
            try:
                submit = self.driver.find_element(By.CSS_SELECTOR, SEL_REPORT_SUBMIT)
                submit.click()
            except NoSuchElementException:
                pass

            time.sleep(0.5)
            return True

        except (NoSuchElementException, TimeoutException):
            return False
