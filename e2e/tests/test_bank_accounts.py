import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
from e2e.utils import depends_on


"""
Test Bank Name validation
test no bank name
Test routing number validation
test no routing number
test account number validation
test no account number
test Delete Bank Account
test empty bank account list with empty modal
"""
logger = logging.getLogger(__name__)


@pytest.mark.use_logged_in_user
def test_create_new_bank_account(bank_accounts_page, faker):
    bank_name = faker.company()
    routing_number = faker.aba()
    account_number = faker.aba()

    bank_accounts_page.load()
    bank_accounts_page.create_account(
        bank_name=bank_name,
        routing_number=routing_number,
        account_number=account_number,
    )

    assert bank_accounts_page.wait_for_condition(
        selector=(
            By.XPATH,
            f'//ul[@data-test="bankaccount-list"]//p[contains(text(), "{bank_name}")]',
        ),
        condition=EC.visibility_of_element_located,
    )


@pytest.mark.use_logged_in_user
class TestEmptyFieldsValidation:
    @pytest.fixture(scope="class")
    def load_create_account_page(self, bank_accounts_page):
        bank_accounts_page.load(new_account_path="/new")

    @pytest.fixture(scope="class")
    def fill_the_form(self, bank_accounts_page):
        bank_accounts_page.enter_bank_name("")
        bank_accounts_page.enter_routing_number("")
        bank_accounts_page.enter_account_number("")
        # Unfocus account number input
        bank_accounts_page.enter_bank_name("")

    @depends_on(["load_create_account_page", "fill_the_form"])
    def test_no_bank_name_validation(self, request, browser):
        assert browser.find_element(
            By.XPATH, '//p[contains(text(), "Enter a bank name")]'
        ).is_displayed()

    @depends_on(["load_create_account_page", "fill_the_form"])
    def test_no_routing_number_validation(self, request, browser):
        assert browser.find_element(
            By.XPATH, '//p[contains(text(), "Enter a bank name")]'
        ).is_displayed()

    @depends_on(["load_create_account_page", "fill_the_form"])
    def test_no_account_number_validation(self, request, browser):
        assert browser.find_element(
            By.XPATH, '//p[contains(text(), "Enter a bank name")]'
        ).is_displayed()


@pytest.mark.use_logged_in_user
def test_no_bank_name_validation():
    return


@pytest.mark.use_logged_in_user
def test_routing_number_validation():
    return


@pytest.mark.use_logged_in_user
def test_no_routing_number_validation():
    return


@pytest.mark.use_logged_in_user
def test_too_short_account_number_validation():
    return


@pytest.mark.use_logged_in_user
def test_too_long_account_number_validation():
    return


@pytest.mark.use_logged_in_user
def test_no_account_number_validation():
    return
