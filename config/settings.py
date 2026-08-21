import os

from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.rokomari.com")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
TEST_USER_NAME = os.getenv("TEST_USER_NAME", "Rok Test 123")
