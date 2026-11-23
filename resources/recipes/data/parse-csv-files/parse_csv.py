"""CSV parsing helpers matching the recipe's patterns.

Run: pytest test_parse_csv.py -v
"""

import csv
import io


def parse_rows(path, delimiter=","):
    """Yield each row as a list of strings."""
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        yield from csv.reader(f, delimiter=delimiter)


def parse_dicts(path, delimiter=","):
    """Yield each row as a dict keyed by header names.

    utf-8-sig strips the BOM Excel writes, so the first column
    name isn't silently corrupted into '\\ufeffname'.
    """
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        yield from csv.DictReader(f, delimiter=delimiter)


def parse_dicts_strict(path):
    """Parse, collecting malformed rows instead of crashing.

    Returns (records, errors) where errors is a list of
    (line_number, row) tuples for rows whose column count
    doesn't match the header.
    """
    records, errors = [], []
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        expected = len(reader.fieldnames or [])
        for row in reader:
            if None in row or len(row) != expected:
                errors.append((reader.line_num, row))
                continue
            records.append(row)
    return records, errors


def sniff_delimiter(path, sample_size=4096):
    """Detect the delimiter of a CSV file (comma, semicolon, tab…)."""
    with open(path, "r", encoding="utf-8-sig") as f:
        sample = f.read(sample_size)
    return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter


def stream_sum(path, column):
    """Sum a numeric column without loading the file into memory."""
    total = 0
    for row in parse_dicts(path):
        try:
            total += int(row[column])
        except (KeyError, TypeError, ValueError):
            continue
    return total
