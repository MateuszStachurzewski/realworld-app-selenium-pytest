import logging
from urllib.parse import urlparse
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def test_successful_signup_and_signin(
    browser, signup_page, signin_page, home_page, faker
):
    first_name = faker.first_name()
    last_name = faker.last_name()
    username = f"{first_name}{last_name}"
    password = faker.password()

    signup_page.load()
    signup_page.sign_up(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        confirm_password=password,
    )

    signin_page.sign_in(username=username, password=password)

    # Assert
    current_path = urlparse(browser.current_url).path
    auth_cookie = browser.get_cookie("connect.sid")

    assert current_path == "/"
    assert auth_cookie["value"] is not None and auth_cookie["value"] != ""
    assert home_page.wait_for_element(
        selector=(By.XPATH, '//div[@data-test="transaction-list"]')
    ).is_displayed()


def test_no_first_name_validation(signup_page):
    signup_page.load()
    signup_page.enter_last_name("LastName")

    assert signup_page.wait_for_element(
        selector=(By.XPATH, '//p[contains(text(), "First Name is required")]')
    ).is_displayed()


def test_no_last_name_validation(signup_page):
    signup_page.load()
    signup_page.enter_last_name("")
    signup_page.enter_username("username")

    assert signup_page.wait_for_element(
        selector=(By.XPATH, '//p[contains(text(), "Last Name is required")]')
    ).is_displayed()


def test_no_username_validation(signup_page):
    signup_page.load()
    signup_page.enter_username("")
    signup_page.enter_password("Password")

    assert signup_page.wait_for_element(
        selector=(By.XPATH, '//p[contains(text(), "Username is required")]')
    ).is_displayed()


def test_no_password_validation(signup_page):
    signup_page.load()
    signup_page.enter_password("")
    signup_page.enter_confirm_password("Password")

    assert signup_page.wait_for_element(
        selector=(By.XPATH, '//p[contains(text(), "Enter your password")]')
    ).is_displayed()


def test_short_password_validation(signup_page):
    signup_page.load()
    signup_page.enter_password("123")

    assert signup_page.wait_for_element(
        selector=(
            By.XPATH,
            '//p[contains(text(), "Password must contain at least 4 characters")]',
        )
    ).is_displayed()


def test_no_confirm_password_validation(signup_page):
    signup_page.load()
    signup_page.enter_confirm_password("")
    signup_page.enter_password("Password")

    assert signup_page.wait_for_element(
        selector=(By.XPATH, '//p[contains(text(), "Confirm your password")]')
    ).is_displayed()


def test_not_matching_confirm_password_validation(signup_page):
    signup_page.load()
    signup_page.enter_confirm_password("Password")

    assert signup_page.wait_for_element(
        selector=(By.XPATH, '//p[contains(text(), "Password does not match")]')
    ).is_displayed()


def test_hyperlink_to_signin_page(browser, signup_page):
    signup_page.load()
    signup_page.click_signin_link()

    assert urlparse(browser.current_url).path == "/signin"
    assert browser.find_element(By.XPATH, '//div[@data-test="signin-username"]')
    assert browser.find_element(By.XPATH, '//div[@data-test="signin-password"]')
