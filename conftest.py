from html import escape

import pytest

from config.settings import TEST_USER_EMAIL, TEST_USER_PASSWORD
from reporting.assertion_reporter import AssertionReporter
from reporting.test_report_manager import TestReportManager


MAX_FAILURE_LINES = 25
FAILURE_TAIL_LINES = 5
FAILED_STEP_ATTRIBUTE = "_failed_assertion_step"
REPORT_MANAGER_KEY = pytest.StashKey[TestReportManager]()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_manager = TestReportManager(
        config.rootpath,
        sensitive_values=(TEST_USER_EMAIL, TEST_USER_PASSWORD),
    )
    report_manager.prepare()
    config.stash[REPORT_MANAGER_KEY] = report_manager


def pytest_html_report_title(report):
    report.title = "Playwright Automation Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append(
        "<p><strong>Security notice:</strong> Failure screenshots and traces "
        "may contain authenticated test-account information.</p>"
    )


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Failed Step</th>")


def pytest_html_results_table_row(report, cells):
    failed_step = escape(getattr(report, "failed_step", "—"))
    cells.insert(2, f"<td>{failed_step}</td>")


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
    report_manager = request.config.stash[REPORT_MANAGER_KEY]

    if terminal_reporter is None:
        def write_terminal_line(message, **_):
            print(message)
    else:
        write_terminal_line = terminal_reporter.write_line

    def write_line(message, **style):
        write_terminal_line(message, **style)
        report_manager.record_step(message)

    def remember_failed_step(label):
        setattr(request.node, FAILED_STEP_ATTRIBUTE, label)

    assertion_reporter = AssertionReporter(
        write_line,
        on_failure=remember_failed_step,
    )

    return assertion_reporter.check


@pytest.hookimpl(wrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    report = yield
    report_manager = item.config.stash[REPORT_MANAGER_KEY]

    if report.failed:
        report_manager.record_failure_details(report)
        failed_step = (
            getattr(item, FAILED_STEP_ATTRIBUTE, None)
            if report.when == "call"
            else None
        )
        report_manager.enrich_failure_report(item, report, failed_step)

    if report.when == "call" or report.failed:
        report_manager.record_test_result(report)

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
