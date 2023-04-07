import logging
from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from e2e.page_objects.common import Common

from e2e.utils import take_screenshot

logger = logging.getLogger(__name__)


class HomePage(Common):
    PATH = "/"

    def load(self):
        try:
            current_path = urlparse(self.browser.current_url).path
            if current_path != self.PATH:
                self.browser.get(f"{self.web_url}{self.PATH}")
        except TimeoutException:
            logger.info("Failed to load Home Page!")
            raise

    def click_bank_accounts_on_side_bar(self):
        try:
            self.browser.find_element(
                By.XPATH, '//a[@data-test="sidenav-bankaccounts"]'
            ).click()
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "click_sign_up_link.png"
            )
            raise

    def logout(self):
        try:
            self.wait_for_redirect(
                method=lambda: self.browser.find_element(
                    By.XPATH,
                    '//div[@data-test="sidenav-signout"]//span[contains(text(), "Logout")]',
                ).click()
            )
        except:
            take_screenshot(self.browser, "e2e/screenshots/home", "logout.png")
            raise
