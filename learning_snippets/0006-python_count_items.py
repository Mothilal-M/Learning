#!/usr/bin/env python3
"""Count how often each hashable item appears in a sequence."""


def count_items(items):
    """Return a dictionary mapping each item to its number of occurrences."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def main():
    values = ["python", "sql", "python", "fastapi", "sql", "python"]
    expected = {"python": 3, "sql": 2, "fastapi": 1}
    assert count_items(values) == expected
    assert count_items([]) == {}
    assert count_items([1, 1, 2]) == {1: 2, 2: 1}

    print(count_items(values))
    print("All examples passed.")


if __name__ == "__main__":
    main()
