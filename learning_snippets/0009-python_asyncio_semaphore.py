#!/usr/bin/env python3
"""Limit concurrent async work with asyncio.Semaphore.

Run:
    python3 learning_snippets/0009-python_asyncio_semaphore.py
"""
import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def gather_limited(
    items: list[T],
    operation: Callable[[T], Awaitable[R]],
    *,
    limit: int,
) -> list[R]:
    """Run async operations with a concurrency limit; preserve input order."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit must be at least 1")

    semaphore = asyncio.Semaphore(limit)

    async def run_one(item: T) -> R:
        async with semaphore:
            return await operation(item)

    return await asyncio.gather(*(run_one(item) for item in items))


async def _self_test() -> None:
    active = 0
    peak_active = 0

    async def fetch_label(item: int) -> str:
        nonlocal active, peak_active
        active += 1
        peak_active = max(peak_active, active)
        try:
            await asyncio.sleep(0.01)
            return f"item-{item}"
        finally:
            active -= 1

    results = await gather_limited(list(range(6)), fetch_label, limit=2)
    assert results == [f"item-{item}" for item in range(6)]
    assert peak_active == 2
    assert active == 0

    async def square(item: int) -> int:
        await asyncio.sleep(0)
        return item * item

    assert await gather_limited([1, 2, 3], square, limit=2) == [1, 4, 9]
    assert await gather_limited([], fetch_label, limit=2) == []

    for invalid_limit in (1.5, True, "2", None):
        try:
            await gather_limited([1], fetch_label, limit=invalid_limit)  # type: ignore[arg-type]
        except TypeError:
            pass
        else:
            raise AssertionError(
                f"limit {invalid_limit!r} should raise TypeError"
            )

    for invalid_limit in (0, -1):
        try:
            await gather_limited([1], fetch_label, limit=invalid_limit)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"limit {invalid_limit} should raise ValueError"
            )

    print("All asyncio semaphore checks passed.")


if __name__ == "__main__":
    asyncio.run(_self_test())
