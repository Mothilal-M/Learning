#!/usr/bin/env python3
"""Remove duplicates from a list while preserving the original order.

Run:
    python3 0005-python_unique_preserve_order.py
"""


def unique_in_order(items):
    """Return the first occurrence of each item, in input order."""
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def main():
    numbers = [3, 1, 3, 2, 1, 4]
    assert unique_in_order(numbers) == [3, 1, 2, 4]
    assert unique_in_order([]) == []
    assert unique_in_order(["a", "a", "b"]) == ["a", "b"]

    print(unique_in_order(numbers))
    print("All examples passed.")


if __name__ == "__main__":
    main()
