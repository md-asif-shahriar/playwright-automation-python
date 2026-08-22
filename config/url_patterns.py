import re

from config.settings import BASE_URL


BASE_URL_PATTERN = re.escape(BASE_URL.rstrip("/"))

HOMEPAGE_URL_PATTERN = re.compile(rf"^{BASE_URL_PATTERN}/?$")
LOGIN_URL_PATTERN = re.compile(
    rf"^{BASE_URL_PATTERN}/login/?(?:[?#].*)?$"
)
