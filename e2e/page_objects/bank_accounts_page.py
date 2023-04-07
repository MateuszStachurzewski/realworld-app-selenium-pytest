import logging
from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException
from e2e.page_objects.common import Common
from selenium.webdriver.common.by import By
from e2e.utils import take_screenshot

logger = logging.getLogger(__name__)


class BankAccountsPage(Common):

    PATH = "/bankaccounts"

    def load(self, new_account_path=""):
        try:
            current_path = urlparse(self.browser.current_url).path
            if current_path != self.PATH:
                logger.info(f"{self.web_url}{self.PATH}")
                self.browser.get(f"{self.web_url}{self.PATH}{new_account_path}")
        except TimeoutException:
            logger.info("Failed to load Bank Accounts Page!")
            raise

    def click_create_button(self):
        try:
            self.wait_for_element(
                selector=(By.XPATH, '//a[@data-test="bankaccount-new"]')
            ).click()
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/bank_accounts", "click_create_button.png"
            )
            raise

    def enter_bank_name(self, bank_name):
        try:
            bank_name_field = self.browser.find_element(
                By.XPATH, '//div[@data-test="bankaccount-bankName-input"]//input'
            )
            bank_name_field.clear()
            bank_name_field.send_keys(bank_name)
        except:
            take_screenshot(
                self.browser, "e2e/screenshots/bank_accounts", "enter_bank_name.png"
            )
            raise

    def enter_routing_number(self, routing_number):
        try:
            routing_number_field = self.browser.find_element(
                By.XPATH, '//div[@data-test="bankaccount-routingNumber-input"]//input'
            )
            routing_number_field.clear()
            routing_number_field.send_keys(routing_number)
        except:
            take_screenshot(
                self.browser,
                "e2e/screenshots/bank_accounts",
                "enter_routing_number.png",
            )
            raise

    def enter_account_number(self, account_number):
        try:
            account_number_field = self.browser.find_element(
                By.XPATH, '//div[@data-test="bankaccount-accountNumber-input"]//input'
            )
            account_number_field.clear()
            account_number_field.send_keys(account_number)
        except:
            take_screenshot(
                self.browser,
                "e2e/screenshots/bank_accounts",
                "enter_account_number.png",
            )
            raise

    def submit_create_account_form(self):
        try:
            self.browser.find_element(
                By.XPATH, '//button[@data-test="bankaccount-submit"]'
            ).click()
        except:
            take_screenshot(
                self.browser,
                "e2e/screenshots/bank_accounts",
                "submit_create_account_form.png",
            )
            raise

    def create_account(self, bank_name, routing_number, account_number):
        self.click_create_button()
        self.enter_bank_name(bank_name)
        self.enter_routing_number(routing_number)
        self.enter_account_number(account_number)
        self.submit_create_account_form()
