from config.settings import BASE_URL


def test_homepage_loads(page):
    page.goto(BASE_URL)

    assert page.url.startswith(BASE_URL)