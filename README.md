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

Expected authenticated display name:

- `TEST_USER_NAME` (defaults to `Rok Test 123`)

Never commit the `.env` file.

## Run Tests

Headless:

pytest

Headed:

pytest --headed

Verbose:

pytest -v

## Failure Diagnostics

Screenshots are retained in the ignored `test-results/` directory only when a
test fails.

Capture a trace for failed tests when deeper debugging is required:

pytest --tracing=retain-on-failure

Show complete failure output without line truncation:

pytest --full-failure-output

Treat screenshots and traces as sensitive artifacts because they may contain
test-account or authenticated-session information.
