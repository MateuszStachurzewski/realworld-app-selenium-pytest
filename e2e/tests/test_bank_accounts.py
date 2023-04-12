import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging
from e2e.utils import depends_on

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
    NO_BANK_NAME_ERR_MSG = (By.XPATH, '//p[contains(text(), "Enter a bank name")]')
    NO_ROUTING_NO_ERR_MSG = (
        By.XPATH,
        '//p[contains(text(), "Enter a valid bank routing number")]',
    )
    NO_ACCOUNT_NO_ERR_MSG = (
        By.XPATH,
        '//p[contains(text(), "Enter a valid bank account number")]',
    )

    @pytest.fixture(scope="class")
    def load_create_account_page(self, bank_accounts_page):
        bank_accounts_page.load(new_account_path="/new")

    @pytest.fixture(scope="class")
    @depends_on(["load_create_account_page"])
    def fill_the_form(self, request, bank_accounts_page):
        bank_accounts_page.enter_bank_name("")
        bank_accounts_page.enter_routing_number("")
        bank_accounts_page.enter_account_number("")
        # Unfocus account number input
        bank_accounts_page.enter_bank_name("")

    @depends_on(["fill_the_form"])
    def test_no_bank_name_validation(self, request, browser):
        assert browser.find_element(*self.NO_BANK_NAME_ERR_MSG).is_displayed()

    @depends_on(["fill_the_form"])
    def test_no_routing_number_validation(self, request, browser):
        assert browser.find_element(*self.NO_ROUTING_NO_ERR_MSG).is_displayed()

    @depends_on(["fill_the_form"])
    def test_no_account_number_validation(self, request, browser):
        assert browser.find_element(*self.NO_ACCOUNT_NO_ERR_MSG).is_displayed()

    @depends_on(["fill_the_form"])
    def test_no_bank_name_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_bank_name(faker.company())
        assert not browser.find_elements(*self.NO_BANK_NAME_ERR_MSG)

    @depends_on(["fill_the_form"])
    def test_no_routing_number_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_routing_number(faker.aba())
        assert not browser.find_elements(*self.NO_ROUTING_NO_ERR_MSG)

    @depends_on(["fill_the_form"])
    def test_no_account_number_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_account_number(faker.aba())
        assert not browser.find_elements(*self.NO_ACCOUNT_NO_ERR_MSG)


@pytest.mark.use_logged_in_user
class TestTooShortBankNameValidation:
    TOO_SHORT_BANK_NAME_ERR_MSG = (
        By.XPATH,
        '//p[contains(text(), "Must contain at least 5 characters")]',
    )

    @pytest.fixture(scope="class")
    def load_create_account_page(self, bank_accounts_page):
        bank_accounts_page.load(new_account_path="/new")

    @pytest.fixture(scope="class")
    @depends_on(["load_create_account_page"])
    def enter_invalid_bank_name(self, request, bank_accounts_page):
        bank_accounts_page.enter_bank_name("test")

    @depends_on(["enter_invalid_bank_name"])
    def test_too_short_bank_name_validation(self, request, browser):
        assert browser.find_element(*self.TOO_SHORT_BANK_NAME_ERR_MSG).is_displayed()

    @depends_on(["enter_invalid_bank_name"])
    def test_too_short_bank_name_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_bank_name(faker.company())
        assert not browser.find_elements(*self.TOO_SHORT_BANK_NAME_ERR_MSG)


@pytest.mark.use_logged_in_user
class TestRoutingNumberValidation:
    INVALID_ROUTING_NO_ERR_MSG = (
        By.XPATH,
        '//p[contains(text(), "Must contain a valid routing number")]',
    )

    @pytest.fixture(scope="class")
    def load_create_account_page(self, bank_accounts_page):
        bank_accounts_page.load(new_account_path="/new")

    @pytest.fixture(scope="class")
    @depends_on(["load_create_account_page"])
    def enter_invalid_routing_number(self, request, bank_accounts_page):
        bank_accounts_page.enter_routing_number("1234")

    @depends_on(["enter_invalid_routing_number"])
    def test_routing_number_validation(self, request, browser):
        assert browser.find_element(*self.INVALID_ROUTING_NO_ERR_MSG).is_displayed()

    @depends_on(["enter_invalid_routing_number"])
    def test_routing_number_validation_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_routing_number(faker.aba())
        assert not browser.find_elements(*self.INVALID_ROUTING_NO_ERR_MSG)


@pytest.mark.use_logged_in_user
class TestTooShortAccountNumberValidation:
    TOO_SHORT_ACCOUNT_NO_ERR_MSG = (
        By.XPATH,
        '//p[contains(text(), "Must contain at least 9 digits")]',
    )

    @pytest.fixture(scope="class")
    def load_create_account_page(self, bank_accounts_page):
        bank_accounts_page.load(new_account_path="/new")

    @pytest.fixture(scope="class")
    @depends_on(["load_create_account_page"])
    def enter_invalid_account_number(self, request, bank_accounts_page):
        bank_accounts_page.enter_account_number("1234")

    @depends_on(["enter_invalid_account_number"])
    def test_too_short_account_number_validation(
        self, request, browser, bank_accounts_page
    ):
        assert browser.find_element(*self.TOO_SHORT_ACCOUNT_NO_ERR_MSG).is_displayed()

    @depends_on(["enter_invalid_account_number"])
    def test_too_short_account_number_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_account_number(faker.aba())
        assert not browser.find_elements(*self.TOO_SHORT_ACCOUNT_NO_ERR_MSG)


@pytest.mark.use_logged_in_user
class TestTooLongAccountNumberValidation:
    TOO_LONG_ACCOUNT_NO_ERR_MSG = (
        By.XPATH,
        '//p[contains(text(), "Must contain no more than 12 digits")]',
    )

    @pytest.fixture(scope="class")
    def load_create_account_page(self, bank_accounts_page):
        bank_accounts_page.load(new_account_path="/new")

    @pytest.fixture(scope="class")
    @depends_on(["load_create_account_page"])
    def enter_invalid_account_number(self, request, bank_accounts_page):
        bank_accounts_page.enter_account_number("1234567891011")

    @depends_on(["enter_invalid_account_number"])
    def test_too_long_account_number_validation(
        self, request, browser, bank_accounts_page
    ):
        assert browser.find_element(*self.TOO_LONG_ACCOUNT_NO_ERR_MSG).is_displayed()

    @depends_on(["enter_invalid_account_number"])
    def test_too_short_account_number_err_msg_disappears(
        self, request, browser, bank_accounts_page, faker
    ):
        bank_accounts_page.enter_account_number(faker.aba())
        assert not browser.find_elements(*self.TOO_LONG_ACCOUNT_NO_ERR_MSG)


@pytest.mark.use_logged_in_user
def test_soft_delete_bank_account(browser, bank_accounts_page):
    bank_accounts_page.load()
    bank_accounts_page.delete_first_bank_account()

    assert browser.find_element(
        By.XPATH,
        '//ul[@data-test="bankaccount-list"][1]//*[contains(p, "(Deleted)")]',
    ).is_displayed()


class TestCreateBankAccountViaModal:
    @pytest.fixture(scope="class")
    def sign_in(self, signin_page, registered_user):
        signin_page.load()
        signin_page.sign_in(username=registered_user.get("username"))

    @pytest.fixture(scope="class")
    def bank_account_data(self, faker):
        bank_name = faker.company()
        routing_number = faker.aba()
        account_number = faker.aba()
        return bank_name, routing_number, account_number

    @pytest.fixture(scope="class")
    @depends_on(["sign_in"])
    def create_account_via_get_started_modal(
        self, request, bank_account_data, get_started_modal
    ):
        (bank_name, routing_number, account_number) = bank_account_data

        get_started_modal.click_next_on_get_started_modal()
        get_started_modal.create_account(
            bank_name=bank_name,
            routing_number=routing_number,
            account_number=account_number,
        )

    @pytest.fixture(scope="class")
    @depends_on(["create_account_via_get_started_modal"])
    def open_bank_accounts_page(self, request, bank_accounts_page):
        bank_accounts_page.load()

    @depends_on(["open_bank_accounts_page"])
    def test_created_account_on_the_list(
        self, request, get_started_modal, bank_account_data
    ):
        (bank_name, *_) = bank_account_data
        assert get_started_modal.wait_for_condition(
            selector=(
                By.XPATH,
                f'//ul[@data-test="bankaccount-list"]//p[contains(text(), "{bank_name}")]',
            ),
            condition=EC.visibility_of_element_located,
        )

    @depends_on(["open_bank_accounts_page"])
    def test_accounst_list_contains_one_account(self, request, browser):
        assert (
            len(
                browser.find_elements(
                    By.XPATH, '//ul[@data-test="bankaccount-list"]/li'
                )
            )
            == 1
        )
