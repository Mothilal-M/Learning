#!/usr/bin/env python3
"""Limit concurrent async work with asyncio.Semaphore.

Run:
    python3 learning_snippets/0009-python_asyncio_semaphore.py
"""
import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def gather_limited(
    items: list[T],
    operation: Callable[[T], Awaitable[str]],
    *,
    limit: int,
) -> list[str]:
    """Run one async operation per item, with at most `limit` active at once."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    semaphore = asyncio.Semaphore(limit)

    async def run_one(item: T) -> str:
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

    assert await gather_limited([], fetch_label, limit=2) == []

    try:
        await gather_limited([1], fetch_label, limit=0)
    except ValueError:
        pass
    else:
        raise AssertionError("limit zero should raise ValueError")

    print("All asyncio semaphore checks passed.")


if __name__ == "__main__":
    asyncio.run(_self_test())
