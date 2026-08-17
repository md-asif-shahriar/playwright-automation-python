# Playwright Automation with Python

A learning-focused UI automation framework built with Playwright, Python, and pytest.

## Tech Stack

- Python
- Playwright
- pytest
- Git / GitHub

## Project Structure

- `tests/` - Test cases
- `pages/` - Page Objects
- `config/` - Test configuration
- `docs/` - Test strategy and documentation
- `conftest.py` - Shared pytest fixtures and configuration

## Setup

Create and activate a virtual environment.

Install dependencies:

pip install -r requirements.txt

Install Chromium:

playwright install chromium

## Environment Variables

Copy `.env.example` to `.env` and provide the required test credentials.

Required variables:

- `BASE_URL`
- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`

Never commit the `.env` file.

## Run Tests

Headless:

pytest

Headed:

pytest --headed

Verbose:

pytest -v