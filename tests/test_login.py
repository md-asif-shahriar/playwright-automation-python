import re

import pytest
from playwright.sync_api import expect

from config.settings import (
    BASE_URL,
    TEST_USER_EMAIL,
    TEST_USER_NAME,
    TEST_USER_PASSWORD,
)
from pages.home_page import HomePage
from pages.login_page import LoginPage


CREDENTIALS_ARE_CONFIGURED = bool(TEST_USER_EMAIL and TEST_USER_PASSWORD)
HOMEPAGE_URL_PATTERN = re.compile(rf"^{re.escape(BASE_URL.rstrip('/'))}/?$")
AUTHENTICATED_UI_TIMEOUT_MS = 30_000


@pytest.mark.skipif(
    not CREDENTIALS_ARE_CONFIGURED,
    reason="TEST_USER_EMAIL and TEST_USER_PASSWORD must be configured",
)
def test_valid_user_can_log_in(page, check_step):
    home_page = HomePage(page, BASE_URL)
    login_page = LoginPage(page)

    home_page.open()

    with check_step("1.1", "Sign In option is visible"):
        expect(home_page.sign_in_link).to_be_visible()

    with check_step("2.1", "Login page URL is correct"):
        home_page.click_sign_in()
        expect(page).to_have_url(re.compile(r".*/login/?(?:[?#].*)?$"))

    with check_step("2.2", "Email field is visible"):
        expect(login_page.email_input).to_be_visible()

    with check_step("2.3", "Next button is visible"):
        expect(login_page.next_button).to_be_visible()

    login_page.enter_email(TEST_USER_EMAIL)

    with check_step("2.4", "Email field contains the test email"):
        email_was_entered = login_page.has_email_value(TEST_USER_EMAIL)
        assert email_was_entered, "Email field did not retain the test email"

    with check_step("2.5", "Next button is enabled"):
        expect(login_page.next_button).to_be_enabled()

    with check_step("2.6", "Password field is visible"):
        login_page.click_next()
        expect(login_page.password_input).to_be_visible(timeout=15_000)

    with check_step("2.7", "Login button is visible"):
        expect(login_page.login_button).to_be_visible()

    login_page.enter_password(TEST_USER_PASSWORD)

    with check_step("2.8", "Login button is enabled"):
        expect(login_page.login_button).to_be_enabled()

    with check_step("3.1", "Homepage URL is correct after login"):
        login_page.submit_login()
        expect(page).to_have_url(
            HOMEPAGE_URL_PATTERN,
            timeout=AUTHENTICATED_UI_TIMEOUT_MS,
        )

    with check_step("3.2", "Sign In option is hidden after login"):
        expect(home_page.sign_in_link).to_be_hidden(
            timeout=AUTHENTICATED_UI_TIMEOUT_MS,
        )

    with check_step("3.3", "Logged-in user name is visible"):
        expect(home_page.get_user_menu_button(TEST_USER_NAME)).to_be_visible(
            timeout=AUTHENTICATED_UI_TIMEOUT_MS,
        )

    with check_step("3.4", '"You Have" text is visible'):
        expect(home_page.points_label).to_be_visible(
            timeout=AUTHENTICATED_UI_TIMEOUT_MS,
        )
