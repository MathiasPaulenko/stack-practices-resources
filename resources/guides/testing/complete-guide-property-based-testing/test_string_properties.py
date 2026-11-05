# Basic property tests with Hypothesis (Python).
# Run: pytest test_string_properties.py -v
from hypothesis import given, strategies as st

@given(st.text())
def test_string_reversal_is_inverse(s):
    """Reversing a string twice gives back the original."""
    assert s[::-1][::-1] == s

@given(st.lists(st.integers()))
def test_list_sort_preserves_length(lst):
    """Sorting a list does not change its length."""
    assert len(sorted(lst)) == len(lst)

@given(st.lists(st.integers()))
def test_list_sort_idempotent(lst):
    """Sorting an already sorted list gives the same list."""
    assert sorted(sorted(lst)) == sorted(lst)

@given(st.lists(st.integers(), min_size=1))
def test_max_is_geq_all(lst):
    """The max of a list is >= all elements."""
    m = max(lst)
    assert all(m >= x for x in lst)
