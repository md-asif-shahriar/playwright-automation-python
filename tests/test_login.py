from playwright.sync_api import expect

from config.settings import (
    BASE_URL,
    TEST_USER_NAME,
)
from config.url_patterns import HOMEPAGE_URL_PATTERN, LOGIN_URL_PATTERN
from pages.home_page import HomePage
from pages.login_page import LoginPage


AUTHENTICATED_UI_TIMEOUT_MS = 30_000


def test_valid_user_can_log_in(page, check_step, login_credentials):
    test_user_email, test_user_password = login_credentials
    home_page = HomePage(page, BASE_URL)
    login_page = LoginPage(page)

    with check_step("1.1", "Sign In option is visible"):
        home_page.open()
        expect(home_page.sign_in_link).to_be_visible()

    with check_step("2.1", "Login page URL is correct"):
        home_page.click_sign_in()
        expect(page).to_have_url(LOGIN_URL_PATTERN)

    with check_step("2.2", "Email field is visible"):
        expect(login_page.email_input).to_be_visible()

    with check_step("2.3", "Next button is visible"):
        expect(login_page.next_button).to_be_visible()

    with check_step("2.4", "Email field contains the test email"):
        login_page.enter_email(test_user_email)
        email_was_entered = login_page.has_email_value(test_user_email)
        assert email_was_entered, "Email field did not retain the test email"

    with check_step("2.5", "Next button is enabled"):
        expect(login_page.next_button).to_be_enabled()

    with check_step("2.6", "Password field is visible"):
        login_page.click_next()
        expect(login_page.password_input).to_be_visible(timeout=15_000)

    with check_step("2.7", "Login button is visible"):
        expect(login_page.login_button).to_be_visible()

    with check_step("2.8", "Login button is enabled"):
        login_page.enter_password(test_user_password)
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
