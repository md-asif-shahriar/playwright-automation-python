import pytest

from reporting.assertion_reporter import AssertionReporter


MAX_FAILURE_LINES = 25


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

    if report.failed and report.longrepr:
        failure_lines = str(report.longrepr).splitlines()

        if len(failure_lines) > MAX_FAILURE_LINES:
            report.longrepr = "\n".join(
                failure_lines[:MAX_FAILURE_LINES]
                + ["... additional failure details truncated ..."]
            )

    return report
