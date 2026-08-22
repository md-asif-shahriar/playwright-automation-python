from playwright.sync_api import Page


EMAIL_KEYSTROKE_DELAY_MS = 50


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.email_input = page.locator("#emailOrPhone")
        self.next_button = page.get_by_role("button", name="পরবর্তী")
        self.password_input = page.get_by_placeholder("পাসওয়ার্ড").or_(
            page.locator('input[name="password"]')
        ).first
        self.login_button = page.get_by_role("button", name="Login", exact=True)

    def enter_email(self, email: str) -> None:
        self.email_input.fill("")
        self.email_input.press_sequentially(
            email,
            delay=EMAIL_KEYSTROKE_DELAY_MS,
        )

    def has_email_value(self, email: str) -> bool:
        return self.email_input.input_value() == email

    def click_next(self) -> None:
        self.next_button.click()

    def enter_password(self, password: str) -> None:
        self.password_input.fill(password)

    def submit_login(self) -> None:
        self.login_button.click()
