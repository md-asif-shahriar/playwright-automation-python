from playwright.sync_api import expect

from config.settings import BASE_URL
from config.url_patterns import LOGIN_URL_PATTERN
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_sign_in_opens_login_page(page, check_step):
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
