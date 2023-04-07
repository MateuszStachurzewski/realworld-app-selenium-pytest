import json
import logging

import pytest
import requests
from selenium import webdriver

from e2e.page_objects.bank_accounts_page import BankAccountsPage
from e2e.page_objects.home_page import HomePage
from e2e.page_objects.signin_page import SignInPage
from e2e.page_objects.signup_page import SignUpPage
from e2e.utils import get_auth_data, take_screenshot
from faker import Faker

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--screenshots", action="store", default=False, help="--debug: True or False"
    )
    parser.addoption(
        "--latency", action="store", default=False, help="--latency: True or False"
    )


@pytest.fixture(scope="session")
def config():
    config_file = open("e2e/config.json")
    config = json.load(config_file)

    assert isinstance(config["web_url"], str)
    assert isinstance(config["api_url"], str)

    return config


@pytest.fixture(scope="session", autouse=True)
def seed_db(config):
    logger.info("Seeding db...")
    url = f'{config["api_url"]}/testData/seed'

    try:
        requests.post(url)
    except Exception as e:
        logging.error("seed_db operation failed!")
        raise e


@pytest.fixture(scope="class")
def browser(request):
    browser = webdriver.Chrome()

    if request.config.getoption("--latency"):
        logger.info("Latency on ...")
        browser.set_network_conditions(
            offline=False,
            latency=1000,
            download_throughput=500 * 1024,
            upload_throughput=500 * 1024,
        )

    yield browser

    if request.config.getoption("--screenshots"):
        logger.info("Screenshots on ...")
        take_screenshot(
            browser, f"e2e/screenshots/{request.node.name}", "finished_at.png"
        )

    browser.quit()


@pytest.fixture(scope="session")
def users(config):
    url = f'{config["api_url"]}/testData/users'

    try:
        resp = requests.get(url)
    except Exception as e:
        logging.error("fetching users from db failed")
        raise e

    return resp.json().get("results")


@pytest.fixture(scope="class")
def signin_page(browser, config):
    return SignInPage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="class")
def signup_page(browser, config):
    return SignUpPage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="class")
def bank_accounts_page(browser, config):
    return BankAccountsPage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="class")
def home_page(browser, config):
    return HomePage(browser=browser, web_url=config["web_url"])


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest.fixture(autouse=True, scope="class")
def use_logged_in_user(request, browser, users, signin_page):
    if "use_logged_in_user" in request.keywords:
        try:
            auth_cookie, auth_state = pytest.auth_data
            signin_page.load()
        except AttributeError:
            auth_cookie, auth_state = get_auth_data(users, browser, signin_page)

        browser.add_cookie({"name": auth_cookie["name"], "value": auth_cookie["value"]})
        browser.execute_script(
            f'return window.localStorage.setItem("authState", {json.dumps(auth_state)})'
        )
