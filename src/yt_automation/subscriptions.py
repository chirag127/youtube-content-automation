"""SubscriptionManager — unsubscribe from channels via Selenium element automation."""

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
YT_SUBSCRIPTIONS_URL = "https://www.youtube.com/feed/channels"

SEL_CHANNEL_ROW = "ytd-channel-renderer"
# The subscribed button shows "Subscribed" as its aria-label or text
ARIA_SUBSCRIBED_BTN = "Unsubscribe"
SEL_SUBSCRIBED_BTN = "ytd-subscribe-button-renderer yt-button-shape button"
# Confirmation dialog "Unsubscribe" button
SEL_CONFIRM_UNSUBSCRIBE = "yt-button-renderer.style-destructive button"
ARIA_CONFIRM_UNSUBSCRIBE = "Unsubscribe"


class SubscriptionManager(BaseAutomation):
    """Manage YouTube channel subscriptions.

    Requires a Chrome profile with an active YouTube login session.
    Set CHROME_PROFILE env var to your Chrome user-data-dir path.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def unsubscribe_all(self, max_channels: int = 500) -> int:
        """Unsubscribe from all channels on the Subscriptions page.

        Scrolls to load channels, then clicks Unsubscribe + confirms
        the dialog for each one.  Returns count unsubscribed.
        """
        self.get(YT_SUBSCRIPTIONS_URL)
        unsubscribed = 0
        last_count = 0

        while unsubscribed < max_channels:
            self.scroll_to_bottom()
            time.sleep(1.5)
            channels = self.driver.find_elements(By.CSS_SELECTOR, SEL_CHANNEL_ROW)
            if len(channels) == last_count:
                break  # no new channels loaded
            last_count = len(channels)

        channels = self.driver.find_elements(By.CSS_SELECTOR, SEL_CHANNEL_ROW)
        for ch in channels[:max_channels]:
            try:
                self.scroll_into_view(ch)
                time.sleep(0.3)
                btn = ch.find_element(By.CSS_SELECTOR, SEL_SUBSCRIBED_BTN)
                if "Subscribed" not in (
                    btn.text or btn.get_attribute("aria-label") or ""
                ):
                    continue
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.5)
                self._confirm_unsubscribe()
                unsubscribed += 1
                time.sleep(0.4)
            except (NoSuchElementException, TimeoutException):
                continue

        return unsubscribed

    def list_subscriptions(self) -> list[str]:
        """Return channel names from the Subscriptions page."""
        self.get(YT_SUBSCRIPTIONS_URL)
        time.sleep(2)
        # Scroll to load all
        for _ in range(20):
            self.scroll_to_bottom()
            time.sleep(1)
        channels = self.driver.find_elements(By.CSS_SELECTOR, SEL_CHANNEL_ROW)
        names: list[str] = []
        for ch in channels:
            try:
                name_el = ch.find_element(By.CSS_SELECTOR, "#channel-title")
                names.append(name_el.text.strip())
            except NoSuchElementException:
                continue
        return names

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _confirm_unsubscribe(self) -> None:
        """Click the destructive Unsubscribe button in the confirmation dialog."""
        try:
            confirm = self._wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//yt-button-renderer[contains(@class,'style-destructive')]//button",
                    )
                )
            )
            confirm.click()
        except TimeoutException:
            pass
