import pytest
import allure
from playwright.sync_api import sync_playwright, Page
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def browser():
   with sync_playwright() as p:
       browser = p.chromium.launch(headless=False)
       yield browser
       browser.close()

@pytest.fixture
def page(browser):
   page = browser.new_page()
   yield page
   page.close()

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """
    A fixture that creates an instance of the LoginPage.
    This instance can be used by any test step.
    """
    return LoginPage(page)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_bdd_after_scenario(request, feature, scenario):
    # Screenshots on step failure (Allure)
    outcome = yield
    if outcome.excinfo:
        page = request.getfixturevalue('page')
        if page:
            allure.attach(page.screenshot(), name="Failure screenshot", attachment_type=allure.attachment_type.PNG)