from collections.abc import Callable, Iterator
from contextlib import contextmanager


class AssertionReporter:
    """Report one final status line for each business-readable assertion."""

    def __init__(
        self,
        write_line: Callable[..., None],
        on_failure: Callable[[str], None] | None = None,
    ):
        self._write_line = write_line
        self._on_failure = on_failure

    @contextmanager
    def check(self, step_number: str, description: str) -> Iterator[None]:
        label = f"#{step_number} {description}"

        try:
            yield
        except Exception:
            if self._on_failure is not None:
                self._on_failure(label)
            self._write_line(f"[FAIL] {label}", red=True)
            raise
        else:
            self._write_line(f"[PASS] {label}", green=True)
