import pytest

from config.settings import TEST_USER_EMAIL, TEST_USER_PASSWORD
from reporting.assertion_reporter import AssertionReporter


MAX_FAILURE_LINES = 25
FAILURE_TAIL_LINES = 5


def pytest_addoption(parser):
    reporting_group = parser.getgroup("reporting")
    reporting_group.addoption(
        "--full-failure-output",
        action="store_true",
        help="Show complete failure details without line truncation.",
    )


@pytest.fixture
def login_credentials() -> tuple[str, str]:
    """Fail clearly when credentials required by login tests are missing."""
    if not TEST_USER_EMAIL or not TEST_USER_PASSWORD:
        pytest.fail(
            "TEST_USER_EMAIL and TEST_USER_PASSWORD must be configured",
            pytrace=False,
        )

    return TEST_USER_EMAIL, TEST_USER_PASSWORD


@pytest.fixture
def check_step(request):
    """Provide a reusable assertion step with one final PASS or FAIL line."""
    terminal_reporter = request.config.pluginmanager.get_plugin("terminalreporter")

    if terminal_reporter is None:
        def write_line(message, **_):
            print(message)
    else:
        write_line = terminal_reporter.write_line

    assertion_reporter = AssertionReporter(write_line)

    return assertion_reporter.check


@pytest.hookimpl(wrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    report = yield

    show_full_failure = item.config.getoption("full_failure_output")

    if report.failed and report.longrepr and not show_full_failure:
        failure_lines = str(report.longrepr).splitlines()

        if len(failure_lines) > MAX_FAILURE_LINES:
            head_line_count = MAX_FAILURE_LINES - FAILURE_TAIL_LINES
            omitted_line_count = len(failure_lines) - MAX_FAILURE_LINES
            report.longrepr = "\n".join(
                failure_lines[:head_line_count]
                + [
                    "... "
                    f"{omitted_line_count} additional failure lines truncated "
                    "..."
                ]
                + failure_lines[-FAILURE_TAIL_LINES:]
            )

    return report
