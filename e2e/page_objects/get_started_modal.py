from e2e.page_objects.common import Common
from selenium.webdriver.common.by import By
from e2e.utils import take_screenshot


class GetStartedModal(Common):
    def click_next_on_get_started_modal(self):
        try:
            self.browser.find_element(
                By.XPATH, '//button[@data-test="user-onboarding-next"]'
            ).click()
        except:
            take_screenshot(
                self.browser,
                "e2e/screenshots/signup",
                "click_next_on_get_started_modal.png",
            )
            raise

    def enter_bank_name(self, bank_name):
        try:
            bank_name_field = self.browser.find_element(
                By.XPATH, '//div[@data-test="bankaccount-bankName-input"]//input'
            )
            self.clear_input(bank_name_field)
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
            self.clear_input(routing_number_field)
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
            self.clear_input(account_number_field)
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
        self.enter_bank_name(bank_name)
        self.enter_routing_number(routing_number)
        self.enter_account_number(account_number)
        self.submit_create_account_form()

    def click_done_on_get_started_modal(self):
        try:
            self.browser.find_element(
                By.XPATH, '//button[@data-test="user-onboarding-next"]'
            ).click()
        except:
            take_screenshot(
                self.browser,
                "e2e/screenshots/signup",
                "click_done_on_get_started_modal.png",
            )
            raise
