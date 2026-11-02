#!/usr/bin/env python3
"""Sum numeric CSV columns from a file or standard input.

Usage:
    python3 0002-python_csv_sums.py data.csv
    cat data.csv | python3 0002-python_csv_sums.py
    python3 0002-python_csv_sums.py --self-test
"""
import argparse
import csv
import sys
from collections.abc import Iterable
from io import StringIO


def sums(reader: Iterable[list[str]]) -> list[float]:
    """Return column totals, treating non-numeric cells as zero."""
    totals: list[float] = []
    for row in reader:
        for index, cell in enumerate(row):
            try:
                value = float(cell)
            except ValueError:
                value = 0.0

            if index >= len(totals):
                totals.append(value)
            else:
                totals[index] += value
    return totals


def _self_test() -> None:
    rows = csv.reader(StringIO("1,2\n3,not-a-number\n4\n,5\n"))
    assert sums(rows) == [8.0, 7.0]
    assert sums(csv.reader(StringIO(""))) == []
    assert sums([["1", "2"], ["3"]]) == [4.0, 2.0]
    print("All CSV sum checks passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sum numeric columns in a CSV.")
    parser.add_argument("path", nargs="?", help="CSV file path (defaults to stdin)")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the built-in checks instead of reading CSV data",
    )
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return

    if args.path is None:
        totals = sums(csv.reader(sys.stdin))
    else:
        with open(args.path, newline="", encoding="utf-8") as source:
            totals = sums(csv.reader(source))

    for index, total in enumerate(totals, start=1):
        print(f"col{index}: {total}")


if __name__ == "__main__":
    main()
