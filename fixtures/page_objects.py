import pytest
from e2e.page_objects.bank_accounts_page import BankAccountsPage
from e2e.page_objects.home_page import HomePage
from e2e.page_objects.signin_page import SignInPage
from e2e.page_objects.signup_page import SignUpPage
from e2e.page_objects.get_started_modal import GetStartedModal


@pytest.fixture(scope="class")
def signin_page(browser, config):
    return SignInPage(
        browser=browser, web_url=config["web_url"], password=config["password"]
    )


@pytest.fixture(scope="class")
def signup_page(browser, config):
    return SignUpPage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="class")
def bank_accounts_page(browser, config):
    return BankAccountsPage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="class")
def home_page(browser, config):
    return HomePage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="class")
def get_started_modal(browser, config):
    return GetStartedModal(browser=browser, web_url=config["web_url"])
