import re

from playwright.sync_api import Locator, Page


class HomePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        self.sign_in_link = page.get_by_role(
            "link",
            name=re.compile(r"sign\s*in", re.IGNORECASE),
        )
        self.points_label = page.get_by_text("You Have", exact=True)

    def open(self) -> None:
        self.page.goto(self.base_url)

    def click_sign_in(self) -> None:
        self.sign_in_link.click()

    def get_user_menu_button(self, user_name: str) -> Locator:
        return self.page.get_by_role(
            "button",
            name=re.compile(re.escape(user_name), re.IGNORECASE),
        )
