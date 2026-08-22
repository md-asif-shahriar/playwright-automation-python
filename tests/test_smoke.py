from playwright.sync_api import expect

from config.settings import BASE_URL
from config.url_patterns import HOMEPAGE_URL_PATTERN


def test_homepage_loads(page, check_step):
    with check_step("1.1", "Homepage URL is correct"):
        page.goto(BASE_URL)
        expect(page).to_have_url(HOMEPAGE_URL_PATTERN)
