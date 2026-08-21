import re

from playwright.sync_api import expect

from config.settings import BASE_URL
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_sign_in_opens_login_page(page, check_step):
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
