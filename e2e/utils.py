import os
import random
from urllib.parse import urlparse
from functools import wraps

import pytest
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def take_screenshot(browser, path, name):
    os.makedirs(path, exist_ok=True)

    screenshot_path = f"{path}/{name}"
    browser.save_screenshot(screenshot_path)
    screenshot = Image.open(screenshot_path)
    screenshot.show()


def wait_for_redirect(browser, method):
    current_url = browser.current_url
    method()
    WebDriverWait(browser, 10).until(EC.url_changes(current_url))


def get_auth_data(users, browser, signin_page):
    user = random.choice(users)
    signin_page.load()
    login = lambda: signin_page.sign_in(username=user.get("username"))
    wait_for_redirect(browser, login)

    auth_cookie = browser.get_cookie("connect.sid")
    auth_state = browser.execute_script(
        'return window.localStorage.getItem("authState")'
    )

    pytest.auth_data = (auth_cookie, auth_state)
    return pytest.auth_data


def depends_on(fixture_names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs["request"]
            for fixture_name in fixture_names:
                request.getfixturevalue(fixture_name)

            return func(*args, **kwargs)

        return wrapper

    return decorator
