"""telegram_extra — leave Telegram groups via Selenium (unrelated to YouTube).

This module is intentionally separate from the YouTube automation classes.
It automates the Telegram Web interface, not the YouTube website.
"""

from __future__ import annotations

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from .base import BaseAutomation

# ---------------------------------------------------------------------------
# Selector constants — Telegram Web (web.telegram.org)
# ---------------------------------------------------------------------------
TG_WEB_URL = "https://web.telegram.org/"

# Group list items in the left sidebar
SEL_CHAT_ITEM = ".chatlist-chat"
# The group name header in the right pane
SEL_CHAT_HEADER = ".chat-info .top .title"
# More actions / three-dot menu in the header
SEL_HEADER_MORE = ".btn-icon.rp[data-peer-id]"
ARIA_MORE = "More"
# "Leave group" option in the context menu
XPATH_LEAVE_ITEM = "//*[contains(@class,'btn-menu-item')][contains(.,'Leave')]"
# Confirmation "Leave" button in the dialog
XPATH_CONFIRM_LEAVE = "//button[contains(@class,'danger')][contains(.,'Leave')]"


class TelegramGroupManager(BaseAutomation):
    """Leave Telegram groups via Telegram Web UI.

    Note: this module is NOT part of the YouTube automation suite.
    It is kept here for historical compatibility only.

    Requires a Chrome profile already logged into web.telegram.org.
    Set CHROME_PROFILE env var to your Chrome user-data-dir path.
    """

    def __init__(self, driver: WebDriver, timeout: int = 20) -> None:
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def leave_all_groups(self, max_groups: int = 200) -> int:
        """Leave up to *max_groups* Telegram groups.

        Opens Telegram Web, iterates the chat list, and leaves each
        group/supergroup via the More-actions menu.
        Returns the count of groups left.
        """
        self.get(TG_WEB_URL)
        time.sleep(5)  # allow Telegram Web to fully load
        left = 0

        for _ in range(max_groups):
            try:
                chats = self.driver.find_elements(By.CSS_SELECTOR, SEL_CHAT_ITEM)
                if not chats:
                    break
                chat = chats[0]
                self.scroll_into_view(chat)
                chat.click()
                time.sleep(0.8)

                if not self._leave_current_group():
                    break
                left += 1
                time.sleep(0.5)
            except (NoSuchElementException, TimeoutException):
                break

        return left

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _leave_current_group(self) -> bool:
        """Leave the currently open group. Returns True on success."""
        try:
            more_btn = self._wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_HEADER_MORE))
            )
            more_btn.click()
            time.sleep(0.4)

            leave_item = self._wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_LEAVE_ITEM))
            )
            leave_item.click()
            time.sleep(0.4)

            confirm_btn = self._wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_CONFIRM_LEAVE))
            )
            confirm_btn.click()
            time.sleep(0.5)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
