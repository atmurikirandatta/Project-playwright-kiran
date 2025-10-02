
# pages/login_page.py
from __future__ import annotations
from playwright.sync_api import Page, Locator,expect
from pages.base_page import BasePage

ORANGE_HRM_LOGIN = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

class LoginPage(BasePage):
    """Login page object using BasePage helpers only."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Inputs – use placeholder-based locators to avoid text collisions
        self.username_input: Locator = self.page.get_by_placeholder("Username")
        self.password_input: Locator = self.page.get_by_placeholder("Password")

        # Labels – target the actual <label> elements to avoid the "Username : Admin" paragraph
        self.username_label: Locator = self.page.locator('label:has-text("Username")')
        self.password_label: Locator = self.page.locator('label:has-text("Password")')

        # Button
        self.login_button: Locator = self.page.get_by_role("button", name="Login")

        #error message
        #self.error_message: Locator = self.page.get_by_text("Invalid credentials")

        #self.username_password_error_messahe: Locator =self.page.get_by_text("Required")



    # -------- actions --------
    def navigate_to_login(self) -> None:
        self.navigate_to_url(ORANGE_HRM_LOGIN)
        # Ensure core controls are present
        self.wait_for_element(self.username_input, state="visible")
        self.wait_for_element(self.password_input, state="visible")
        self.wait_for_element(self.login_button, state="visible")

    def verify_all_fields(self) -> None:
        # Waits also serve as assertions here
        self.wait_for_element(self.username_label, state="visible")
        self.wait_for_element(self.username_input, state="visible")
        self.wait_for_element(self.password_label, state="visible")
        self.wait_for_element(self.password_input, state="visible")
        self.wait_for_element(self.login_button, state="visible")

    def enter_username(self, username: str) -> None:
        self.type_text(self.username_input, username)          

    def enter_password(self, password: str) -> None:
        # Skip value verification for password fields
        self.fill_text(self.password_input, password, verify=False, sensitive=True)

    def click_login(self) -> None:
        self.click_element(self.login_button)
        #self.page.wait_for_timeout(1000)

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def error_message_label(self, Error_Message):

        self.error_message: Locator = self.page.get_by_text(Error_Message)
        self.wait_for_element(self.error_message)
        self.is_element_visible(self.error_message)
    