from config.settings import BASE_URL


def test_homepage_loads(page, check_step):
    page.goto(BASE_URL)

    with check_step("1.1", "Homepage URL is correct"):
        assert page.url.startswith(BASE_URL)
