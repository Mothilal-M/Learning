"""Retry a transient operation with bounded exponential backoff.

Run the examples and tests with:
    python learning_snippets/0008-python_retry_backoff.py
"""
from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    initial_delay: float = 0.1,
    retry_on: tuple[type[Exception], ...] = (TimeoutError, ConnectionError),
    wait: Callable[[float], None] = sleep,
) -> T:
    """Retry selected transient errors, doubling the delay after each failure."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    if initial_delay < 0:
        raise ValueError("initial_delay cannot be negative")

    for attempt in range(attempts):
        try:
            return operation()
        except retry_on:
            if attempt == attempts - 1:
                raise
            wait(initial_delay * (2**attempt))

    raise AssertionError("unreachable")


def _self_test() -> None:
    delays: list[float] = []
    calls = 0

    def flaky_operation() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise TimeoutError("temporary timeout")
        return "ok"

    assert retry(flaky_operation, initial_delay=0.25, wait=delays.append) == "ok"
    assert calls == 3
    assert delays == [0.25, 0.5]

    calls = 0

    def always_fails() -> None:
        nonlocal calls
        calls += 1
        raise ConnectionError("still unavailable")

    try:
        retry(always_fails, attempts=2, wait=delays.append)
    except ConnectionError:
        pass
    else:
        raise AssertionError("the final error should be re-raised")
    assert calls == 2

    try:
        retry(lambda: 1 / 0)
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("unexpected errors must not be retried")

    print("All retry/backoff checks passed.")


if __name__ == "__main__":
    _self_test()
