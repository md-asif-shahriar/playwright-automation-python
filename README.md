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

Every test run generates the following ignored local reports:

- `reports/report.html` - human-readable, self-contained HTML report
- `reports/junit.xml` - machine-readable JUnit report
- `reports/execution.log` - sanitized assertion and test status log

Open the HTML report from Git Bash after a test run:

explorer.exe reports/report.html

Screenshots and traces are retained in the ignored `test-results/` directory
only when a test fails. A viewport screenshot is also embedded in the HTML
report when the Playwright page is still available.

Failure trace capture is enabled by default. To explicitly run with the same
setting:

pytest --tracing=retain-on-failure

Show complete failure output without line truncation:

pytest --full-failure-output

Treat screenshots and traces as sensitive artifacts because they may contain
test-account or authenticated-session information. The generated `reports/`
directory must be treated as sensitive for the same reason.

For purpose-based setup, execution, reporting, screenshot, and trace commands,
see `docs/test-reporting-commands.md`.
