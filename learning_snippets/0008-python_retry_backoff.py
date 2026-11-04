"""Retry a transient operation with capped exponential backoff.

Run the examples and tests with:
    python learning_snippets/0008-python_retry_backoff.py
"""
import math
from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def _validate_delay(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    try:
        delay = float(value)
    except OverflowError:
        raise ValueError(f"{name} must be finite") from None
    if not math.isfinite(delay):
        raise ValueError(f"{name} must be finite")
    if delay < 0:
        raise ValueError(f"{name} cannot be negative")
    return delay


def retry(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    initial_delay: float = 0.1,
    max_delay: float = 30.0,
    retry_on: tuple[type[Exception], ...] = (TimeoutError, ConnectionError),
    wait: Callable[[float], None] = sleep,
) -> T:
    """Retry selected transient errors with a capped exponential delay."""
    if isinstance(attempts, bool) or not isinstance(attempts, int):
        raise TypeError("attempts must be an integer")
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    max_delay_value = _validate_delay("max_delay", max_delay)
    delay = min(_validate_delay("initial_delay", initial_delay), max_delay_value)

    for attempt in range(attempts):
        try:
            return operation()
        except retry_on:
            if attempt == attempts - 1:
                raise
            wait(delay)
            delay = min(delay * 2, max_delay_value)

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

    def expect_error(error_type: type[Exception], **kwargs: object) -> None:
        try:
            retry(lambda: "unused", **kwargs)  # type: ignore[arg-type]
        except error_type:
            return
        raise AssertionError(f"expected {error_type.__name__} for {kwargs!r}")

    for invalid_attempts in (1.5, True, "3", None):
        expect_error(TypeError, attempts=invalid_attempts)
    for invalid_attempts in (0, -1):
        expect_error(ValueError, attempts=invalid_attempts)

    for invalid_delay in ("0.1", True, None):
        expect_error(TypeError, initial_delay=invalid_delay)
    for invalid_delay in (-0.1, math.nan, math.inf, -math.inf, 10**1000):
        expect_error(ValueError, initial_delay=invalid_delay)

    delays.clear()
    calls = 0

    def eventually_succeeds() -> str:
        nonlocal calls
        calls += 1
        if calls < 4:
            raise TimeoutError("temporary timeout")
        return "done"

    assert retry(
        eventually_succeeds,
        attempts=4,
        initial_delay=0.5,
        max_delay=0.75,
        wait=delays.append,
    ) == "done"
    assert delays == [0.5, 0.75, 0.75]

    for invalid_delay in ("1", True, None):
        expect_error(TypeError, max_delay=invalid_delay)
    for invalid_delay in (-1, math.nan, math.inf, 10**1000):
        expect_error(ValueError, max_delay=invalid_delay)

    print("All retry/backoff checks passed.")


if __name__ == "__main__":
    _self_test()
