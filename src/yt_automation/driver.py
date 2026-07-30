"""WebDriver factory — shared Chrome/Firefox driver with profile/cookies support."""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_WAIT = 15  # seconds


def build_driver(
    *,
    headless: bool = False,
    profile_dir: str | Path | None = None,
    window_size: tuple[int, int] = (1280, 900),
) -> webdriver.Chrome:
    """Return a configured Chrome WebDriver.

    Args:
        headless: Run without a visible browser window.
        profile_dir: Path to a Chrome user-data-dir that holds login cookies.
                     If None, uses CHROME_PROFILE env var, then a temp profile.
        window_size: (width, height) in pixels.
    """
    opts = ChromeOptions()

    if headless:
        opts.add_argument("--headless=new")

    _profile = profile_dir or os.environ.get("CHROME_PROFILE")
    if _profile:
        opts.add_argument(f"--user-data-dir={_profile}")

    opts.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(DEFAULT_WAIT)
    return driver


def wait(driver: webdriver.Chrome, timeout: int = DEFAULT_WAIT) -> WebDriverWait:
    """Convenience wrapper around WebDriverWait."""
    return WebDriverWait(driver, timeout)
