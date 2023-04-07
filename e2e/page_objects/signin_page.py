import logging
from urllib.parse import urlparse

from e2e.page_objects.common import Common
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from e2e.utils import take_screenshot

logger = logging.getLogger(__name__)


class SignInPage(Common):
    PATH = "/signin"
    PASSWORD = "s3cret"

    def load(self):
        try:
            current_path = urlparse(self.browser.current_url).path

            if current_path != self.PATH:
                self.browser.get(f"{self.web_url}{self.PATH}")
        except TimeoutException:
            logger.info("Failed to load Signin Page!")
            raise

    def enter_username(self, username):
        try:
            username_field = self.browser.find_element(
                By.CSS_SELECTOR, 'div[data-test="signin-username"]'
            ).find_element(By.CSS_SELECTOR, 'input[id="username"]')
            username_field.clear()
            username_field.send_keys(username)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signin", "enter_username.png"
            )
            raise

    def enter_password(self, password):
        try:
            username_field = self.browser.find_element(
                By.CSS_SELECTOR, 'div[data-test="signin-password"]'
            ).find_element(By.CSS_SELECTOR, 'input[id="password"]')
            username_field.clear()
            username_field.send_keys(password)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signin", "enter_password.png"
            )
            raise

    def check_remember_me(self):
        try:
            self.browser.find_element(
                By.XPATH, '//span[@data-test="signin-remember-me"]'
            ).click()
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signin", "check_remember_me.png"
            )
            raise

    def click_sign_in(self):
        try:
            self.browser.find_element(
                By.XPATH, '//button[@data-test="signin-submit"]'
            ).click()

        except:
            take_screenshot(self.browser, "e2e/screenshots/signin", "sign_in.png")
            raise

    def click_signup_link(self):
        try:
            el = self.browser.find_element(By.XPATH, '//a[@data-test="signup"]')
            self.wait_for_redirect(
                method=lambda: self.browser.execute_script("arguments[0].click();", el)
            )
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signin", "click_sign_up_link.png"
            )
            raise

    def sign_in(
        self, username, password=PASSWORD, remember_me=False, wait_for_redirect=True
    ):
        self.enter_username(username)
        self.enter_password(password)
        if remember_me:
            self.check_remember_me()

        if wait_for_redirect:
            return self.wait_for_redirect(method=lambda: self.click_sign_in())
        self.click_sign_in()
