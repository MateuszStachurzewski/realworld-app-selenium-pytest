import json
import pytest
import logging
import requests
from e2e.utils import get_auth_data

logger = logging.getLogger(__name__)


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


@pytest.fixture(scope="class")
def registered_user(config, faker):
    url = f'{config["api_url"]}/users'
    password = config["password"]

    first_name = faker.first_name()
    last_name = faker.last_name()
    username = f"{first_name}{last_name}"

    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "password": password,
        "confirmPassword": password,
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        logging.error("seed_db operation failed!")
        raise e

    return payload
