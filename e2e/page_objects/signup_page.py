import logging
from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from e2e.page_objects.common import Common
from selenium.webdriver.support import expected_conditions as EC

from e2e.utils import take_screenshot

logger = logging.getLogger(__name__)


class SignUpPage(Common):
    PATH = "/signup"

    def load(self):
        try:
            current_path = urlparse(self.browser.current_url).path

            if current_path != self.PATH:
                self.browser.get(f"{self.web_url}{self.PATH}")
        except TimeoutException:
            logger.info("Failed to load Signup Page!")
            raise

    def enter_first_name(self, first_name):
        try:
            first_name_field = self.browser.find_element(
                By.XPATH, '//input[@id="firstName"]'
            )
            first_name_field.clear()
            first_name_field.send_keys(first_name)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "enter_first_name.png"
            )
            raise

    def enter_last_name(self, last_name):
        try:
            last_name_field = self.browser.find_element(
                By.XPATH, '//input[@id="lastName"]'
            )
            last_name_field.clear()
            last_name_field.send_keys(last_name)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "enter_last_name.png"
            )
            raise

    def enter_username(self, username):
        try:
            username_field = self.browser.find_element(
                By.XPATH, '//input[@id="username"]'
            )
            username_field.clear()
            username_field.send_keys(username)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "enter_username.png"
            )
            raise

    def enter_password(self, password):
        try:
            password_field = self.browser.find_element(
                By.XPATH, '//input[@id="password"]'
            )
            password_field.clear()
            password_field.send_keys(password)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "enter_password.png"
            )
            raise

    def enter_confirm_password(self, password):
        try:
            confirm_password_field = self.browser.find_element(
                By.XPATH, '//input[@id="confirmPassword"]'
            )
            confirm_password_field.clear()
            confirm_password_field.send_keys(password)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "enter_confirm_password.png"
            )
            raise

    def click_sign_up(self):
        try:
            self.wait_for_condition(
                selector=(By.XPATH, '//button[@data-test="signup-submit"]'),
                condition=EC.element_to_be_clickable,
            ).click()
        except:
            take_screenshot(self.browser, "e2e/screenshots/signup", "sign_up.png")
            raise

    def click_signin_link(self):
        try:
            el = self.browser.find_element(By.XPATH, '//a[@href="/signin"]')
            self.wait_for_redirect(
                method=lambda: self.browser.execute_script("arguments[0].click();", el)
            )
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/signup", "click_sign_up_link.png"
            )
            raise

    def sign_up(
        self,
        first_name,
        last_name,
        username,
        password,
        confirm_password,
        wait_for_redirect=True,
    ):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        if wait_for_redirect:
            return self.wait_for_redirect(method=lambda: self.click_sign_up())
        self.click_sign_up()
