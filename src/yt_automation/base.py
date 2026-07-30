"""BaseAutomation — shared element-find/click/wait helpers."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15


class BaseAutomation:
    """Common helpers for all automation classes.

    Subclasses receive a driver at construction time; all element
    interactions go through the methods here so selectors stay
    centralised and waits are consistent.
    """

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def get(self, url: str) -> None:
        self.driver.get(url)

    # ------------------------------------------------------------------
    # Element finders
    # ------------------------------------------------------------------

    def find(self, css: str) -> WebElement:
        """Wait for element by CSS selector and return it."""
        return self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))

    def find_clickable(self, css: str) -> WebElement:
        return self._wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))

    def find_by_xpath(self, xpath: str) -> WebElement:
        return self._wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def find_by_aria(self, label: str) -> WebElement:
        return self._wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@aria-label="{label}"]'))
        )

    def find_all(self, css: str) -> list[WebElement]:
        self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        return self.driver.find_elements(By.CSS_SELECTOR, css)

    # ------------------------------------------------------------------
    # Interactions
    # ------------------------------------------------------------------

    def click(self, css: str) -> None:
        self.find_clickable(css).click()

    def click_aria(self, label: str) -> None:
        self.find_by_aria(label).click()

    def type_into(self, css: str, text: str) -> None:
        el = self.find(css)
        el.clear()
        el.send_keys(text)

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_into_view(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
