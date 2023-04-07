import datetime
import logging
import random
from urllib.parse import urlparse

import pytest
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def test_successful_login(browser, users, signin_page):
    # Arrange
    user = random.choice(users)
    signin_page.load()

    # Act
    signin_page.sign_in(username=user.get("username"))

    # Assert
    current_path = urlparse(browser.current_url).path
    cookie = browser.get_cookie("connect.sid")

    assert current_path == "/"
    assert "expiry" not in cookie


def test_user_is_remembered_for_30_days_after_login(browser, signin_page, users):
    # Arrange
    user = random.choice(users)
    signin_page.load()

    # Act
    signin_page.sign_in(username=user.get("username"), remember_me=True)

    # Assert
    cookie = browser.get_cookie("connect.sid")
    month_from_now = datetime.datetime.now() + datetime.timedelta(30)

    assert (
        datetime.datetime.fromtimestamp(cookie["expiry"]).date()
        == month_from_now.date()
    )


def test_unsuccessful_login(browser, signin_page):
    # Arrange
    signin_page.load()

    # Act
    signin_page.sign_in(
        username="incorrect@gmail.com", password="password", wait_for_redirect=False
    )

    # Assert
    assert signin_page.wait_for_element(
        selector=(
            By.XPATH,
            '//div[@data-test="signin-error"]/div[contains(text(), "Username or password is invalid")]',
        )
    ).is_displayed()

    assert urlparse(browser.current_url).path == "/signin"


def test_no_username_validation(browser, signin_page):
    # Arrange
    signin_page.load()

    # Act
    signin_page.click_sign_in()

    # Assert
    assert signin_page.wait_for_element(
        selector=(
            By.XPATH,
            '//div[@data-test="signin-username"]//p[contains(text(), "Username is required")]',
        )
    ).is_displayed()


def test_short_password_validation(browser, signin_page):
    # Arrange
    signin_page.load()

    # Act
    signin_page.enter_password("123")
    signin_page.check_remember_me()

    # Assert
    assert signin_page.wait_for_element(
        selector=(
            By.XPATH,
            '//div[@data-test="signin-password"]//p[contains(text(), "Password must contain at least 4 characters")]',
        )
    ).is_displayed()


def test_unauthenticated_user_is_redirected_to_signin_page(browser, bank_accounts_page):
    # Act
    bank_accounts_page.load()

    # Assert
    current_path = urlparse(browser.current_url).path

    assert browser.find_element(
        By.XPATH, '//div[@data-test="signin-username"]'
    ).is_displayed()

    assert current_path == "/signin"


@pytest.mark.use_logged_in_user
def test_authenticated_user_can_log_out(browser, home_page):
    # Arrange
    home_page.load()

    # Act
    home_page.logout()

    # Assert
    current_path = urlparse(browser.current_url).path
    cookie = browser.get_cookie("connect.sid")

    assert browser.find_element(
        By.XPATH, '//div[@data-test="signin-username"]'
    ).is_displayed()
    assert current_path == "/signin"
    assert cookie is None


def test_hyperlink_to_signup_page(browser, signin_page):
    # Arrange
    signin_page.load()

    # Act
    signin_page.click_signup_link()

    # Assert
    assert urlparse(browser.current_url).path == "/signup"
    assert browser.find_element(By.XPATH, '//div[@data-test="signup-first-name"]')
    assert browser.find_element(By.XPATH, '//div[@data-test="signup-last-name"]')
    assert browser.find_element(By.XPATH, '//div[@data-test="signup-username"]')
    assert browser.find_element(By.XPATH, '//div[@data-test="signup-password"]')
    assert browser.find_element(By.XPATH, '//div[@data-test="signup-confirmPassword"]')
