#!/usr/bin/env python3
"""Split an iterable into small lists without loading it all at once.

Run:
    python3 learning_snippets/0007-python_chunked.py
"""


def chunked(items, size):
    """Yield lists of at most size items; size must be a positive integer."""
    if size <= 0:
        raise ValueError("size must be greater than zero")

    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def main():
    records = ["user-1", "user-2", "user-3", "user-4", "user-5"]
    assert list(chunked(records, 2)) == [
        ["user-1", "user-2"],
        ["user-3", "user-4"],
        ["user-5"],
    ]
    assert list(chunked([], 3)) == []
    assert list(chunked([1, 2], 2)) == [[1, 2]]
    assert list(chunked((number for number in range(3)), 5)) == [[0, 1, 2]]

    try:
        list(chunked([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("chunk size zero should raise ValueError")

    print(list(chunked(records, 2)))
    print("All examples passed.")


if __name__ == "__main__":
    main()
