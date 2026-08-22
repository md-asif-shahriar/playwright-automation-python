from collections.abc import Callable, Iterator
from contextlib import contextmanager


class AssertionReporter:
    """Report one final status line for each business-readable assertion."""

    def __init__(self, write_line: Callable[..., None]):
        self._write_line = write_line

    @contextmanager
    def check(self, step_number: str, description: str) -> Iterator[None]:
        label = f"#{step_number} {description}"

        try:
            yield
        except Exception:
            self._write_line(f"[FAIL] {label}", red=True)
            raise
        else:
            self._write_line(f"[PASS] {label}", green=True)
