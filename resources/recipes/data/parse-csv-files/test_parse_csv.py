"""Tests for the parse_csv helpers. Run: pytest test_parse_csv.py -v"""

from pathlib import Path

from parse_csv import (
    parse_dicts,
    parse_dicts_strict,
    parse_rows,
    sniff_delimiter,
    stream_sum,
)

HERE = Path(__file__).parent


def test_parse_rows():
    rows = list(parse_rows(HERE / "sample.csv"))
    assert rows[0] == ["name", "email", "age"]
    assert len(rows) == 4


def test_quoted_field_with_comma():
    """split(',') would break this row; csv.reader doesn't."""
    rows = list(parse_rows(HERE / "sample.csv"))
    assert rows[2][1] == "b@x.com, inc"


def test_dict_reader_by_name():
    recs = list(parse_dicts(HERE / "sample.csv"))
    assert recs[0]["name"] == "alice"
    assert recs[0]["email"] == "a@x.com"


def test_bom_is_stripped():
    recs = list(parse_dicts(HERE / "sample_bom.csv"))
    assert "name" in recs[0]
    assert "﻿name" not in recs[0]


def test_sniff_semicolon():
    assert sniff_delimiter(HERE / "sample_semicolon.csv") == ";"


def test_semicolon_parse():
    recs = list(parse_dicts(HERE / "sample_semicolon.csv",
                            delimiter=sniff_delimiter(HERE / "sample_semicolon.csv")))
    assert recs[0]["name"] == "frank"


def test_strict_collects_bad_rows(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("name,email\nok,a@x.com\ntoo,many,cols,b@x.com\n", encoding="utf-8")
    records, errors = parse_dicts_strict(bad)
    assert len(records) == 1
    assert len(errors) == 1


def test_stream_sum():
    assert stream_sum(HERE / "sample.csv", "age") == 30 + 41 + 28
