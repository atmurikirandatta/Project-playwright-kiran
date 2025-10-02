"""User Authentication feature tests."""
import pytest
import allure
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage
# Add 'expect' to your import line
from playwright.sync_api import Page, expect

# Load all scenarios from authentication features
scenarios('../Features/login.feature')

@given('the user is on the login page')
@allure.step("User navigates to login page")
def navigate_to_login_page(login_page: LoginPage):
    """Navigate to the login page."""
    login_page.navigate_to_login()


@when('the user clicks the login button')
@allure.step("Click login button")
def click_login_button(login_page: LoginPage):
    """Click the login button."""
    login_page.click_login()



@when(parsers.re(r'^the user enters invalid password "(?P<password>.*)"$'))
@allure.step("Enter invalid password: ***")
def enter_wrong_password(login_page: LoginPage, password: str):
    """the user enters invalid password "wrong_password"."""
    if password:
        login_page.enter_password(password)

@when(parsers.re(r'^the user enters invalid username "(?P<username>.*)"$'))
@allure.step("Enter invalid username: {username}")
def enter_invalid_username(login_page: LoginPage, username: str):

    if username:
        login_page.enter_username(username)


@when(parsers.parse('the user enters valid password "{password}"'))
@allure.step("Enter valid password: ***")
def enter_valid_password(login_page: LoginPage , password: str):
    login_page.enter_password(password)


@when(parsers.parse('the user enters valid username "{username}"'))
@allure.step("Enter valid username: {username}")
def enter_valid_username(login_page: LoginPage, username: str):
    login_page.enter_username(username)


@then('the user should land on the landing page')
@allure.step("Check if landed on home")
def _(login_page: LoginPage):
    login_page.page.wait_for_timeout(5000)


@then('the user should remain on the login page')
@allure.step("Remain on login page")
def login_page(login_page: LoginPage):
    expect(login_page.page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")


@then(parsers.re(r'the user should see error message "(?P<expected_error>.+)"'))
@allure.step("Check error message: {expected_error}")
def error_message(login_page: LoginPage, expected_error ):
    login_page.error_message_label(expected_error)

