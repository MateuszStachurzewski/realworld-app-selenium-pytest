from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Common:
    def __init__(self, browser, web_url):
        self.browser = browser
        self.web_url = web_url

    def wait_for_redirect(self, method):
        current_url = self.browser.current_url
        method()
        WebDriverWait(self.browser, 10).until(EC.url_changes(current_url))

    def wait_for_element(self, selector):
        return WebDriverWait(self.browser, 10).until(
            lambda browser: browser.find_element(*selector)
        )

    def wait_for_condition(self, selector, condition):
        return WebDriverWait(self.browser, 10).until(condition(selector))
