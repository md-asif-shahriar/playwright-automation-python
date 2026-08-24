from base64 import b64encode
from pathlib import Path
from typing import Any, Iterable

from pytest_html import extras


REPORTS_DIRECTORY_NAME = "reports"
EXECUTION_LOG_NAME = "execution.log"
NO_FAILED_STEP = "—"


class TestReportManager:
    """Create sanitized logs and enrich pytest reports with failure context."""

    def __init__(
        self,
        project_root: Path,
        sensitive_values: Iterable[str | None] = (),
    ):
        self.reports_directory = project_root / REPORTS_DIRECTORY_NAME
        self.execution_log = self.reports_directory / EXECUTION_LOG_NAME
        self._sensitive_values = tuple(
            value for value in sensitive_values if value
        )

    def prepare(self) -> None:
        self.reports_directory.mkdir(parents=True, exist_ok=True)
        self.execution_log.write_text(
            "Playwright automation execution log\n",
            encoding="utf-8",
        )

    def record_step(self, message: str) -> None:
        """Record only predefined assertion labels, never entered test data."""
        self._append_line(message)

    def record_test_result(self, report: Any) -> None:
        if report.when == "call":
            status = report.outcome.upper()
            self._append_line(f"[TEST {status}] {report.nodeid}")
        elif report.failed:
            self._append_line(
                f"[TEST ERROR] {report.nodeid} ({report.when})"
            )

    def record_failure_details(self, report: Any) -> None:
        if not report.longrepr:
            return

        original_failure = str(report.longrepr)
        sanitized_failure = self._redact(original_failure)

        self._append_line(
            "\n"
            f"[FAILURE DETAILS] {report.nodeid} ({report.when})\n"
            f"{sanitized_failure}\n"
            "[END FAILURE DETAILS]"
        )

        if sanitized_failure != original_failure:
            report.longrepr = sanitized_failure

    def enrich_failure_report(
        self,
        item: Any,
        report: Any,
        failed_step: str | None,
    ) -> None:
        report.failed_step = failed_step or NO_FAILED_STEP

        report_extras = list(getattr(report, "extras", []))

        if failed_step:
            user_properties = list(
                getattr(report, "user_properties", [])
            )
            user_properties.append(("failed_assertion_step", failed_step))
            report.user_properties = user_properties
            report.sections.append(("Failed assertion step", failed_step))
            report_extras.append(
                extras.text(failed_step, name="Failed assertion step")
            )

        report_extras.append(
            extras.text(
                "Original Playwright failure artifacts are stored under "
                "test-results/ when available.",
                name="Failure artifacts",
            )
        )

        screenshot = self._capture_viewport_screenshot(item)
        if screenshot is not None:
            encoded_screenshot = b64encode(screenshot).decode("ascii")
            report_extras.append(
                extras.png(
                    encoded_screenshot,
                    name="Failure screenshot",
                )
            )

        report.extras = report_extras

    @staticmethod
    def _capture_viewport_screenshot(item: Any) -> bytes | None:
        page = getattr(item, "funcargs", {}).get("page")

        if page is None:
            return None

        try:
            if page.is_closed():
                return None
            return page.screenshot()
        except Exception:
            # Diagnostics must never replace the original test failure.
            return None

    def _append_line(self, message: str) -> None:
        try:
            with self.execution_log.open("a", encoding="utf-8") as log_file:
                log_file.write(f"{message}\n")
        except OSError:
            # Reporting must not turn an application assertion into a new error.
            return

    def _redact(self, message: str) -> str:
        sanitized_message = message

        for sensitive_value in self._sensitive_values:
            sanitized_message = sanitized_message.replace(
                sensitive_value,
                "[REDACTED]",
            )

        return sanitized_message
