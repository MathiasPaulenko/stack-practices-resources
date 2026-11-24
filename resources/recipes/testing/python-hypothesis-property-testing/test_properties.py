"""Property-based tests with Hypothesis.

Companion code for https://stackpractices.com/recipes/python-hypothesis-property-testing/

Requirements:
    pip install -r requirements.txt

Usage:
    pytest test_properties.py -v
"""

import json
import math

from hypothesis import assume, example, given, settings
from hypothesis import strategies as st


def reverse_string(s: str) -> str:
    return s[::-1]


@given(st.text())
def test_reverse_twice_returns_original(s):
    assert reverse_string(reverse_string(s)) == s


@given(st.text())
def test_reverse_preserves_length(s):
    assert len(reverse_string(s)) == len(s)


@given(st.text())
def test_reverse_first_becomes_last(s):
    if s:
        assert reverse_string(s)[0] == s[-1]


@given(st.integers(min_value=0, max_value=100))
def test_square_is_non_negative(n):
    assert n * n >= 0


@given(st.integers(), st.integers())
def test_addition_is_commutative(a, b):
    assert a + b == b + a


@given(st.integers(min_value=1))
def test_division_then_multiplication(n):
    assert (n * 10) // 10 == n


@given(st.lists(st.integers(min_value=1, max_value=100), min_size=1))
def test_max_is_in_list(lst):
    assert max(lst) in lst


@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    assert len(sorted(lst)) == len(lst)


@given(st.lists(st.integers()))
def test_sort_is_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)


@given(st.lists(st.integers(), min_size=1))
def test_min_le_max(lst):
    assert min(lst) <= max(lst)


@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_dict_items_roundtrip(d):
    assert dict(d.items()) == d


@given(st.from_type(dict))
def test_json_roundtrip(d):
    encoded = json.dumps(d)
    decoded = json.loads(encoded)
    assert decoded == d


@given(st.integers())
def test_division(n):
    assume(n != 0)
    # Float division isn't exact — compare with tolerance, not ==
    assert math.isclose(100 / n * n, 100)


@given(st.lists(st.integers()))
def test_sorted_min_is_first(lst):
    assume(len(lst) > 0)
    assert min(lst) == sorted(lst)[0]


@given(st.lists(st.integers()))
@example([])
@example([1])
@example([1, 2, 3])
def test_sort_with_specific_cases(lst):
    assert sorted(lst) == sorted(sorted(lst))


@given(st.lists(st.integers()))
@settings(max_examples=500, deadline=1000)
def test_with_more_examples(lst):
    assert sorted(lst) == sorted(lst, reverse=True)[::-1]
