"""Property-based testing examples with Hypothesis.

Run with: pytest test_property_based.py -v
"""
import json

from hypothesis import given, strategies as st
from hypothesis.stateful import (
    RuleBasedStateMachine,
    invariant,
    precondition,
    rule,
)


def reverse(s: str) -> str:
    return s[::-1]


# Basic property: reversing twice returns the original
@given(st.text())
def test_reverse_is_involution(s):
    assert reverse(reverse(s)) == s


# Constrained strategy
@given(st.integers(min_value=0, max_value=1000))
def test_square_is_non_negative(n):
    assert n * n >= 0


# Composite strategy for domain objects
@st.composite
def users(draw):
    return {
        "name": draw(st.text(min_size=1, max_size=100)),
        "age": draw(st.integers(min_value=0, max_value=150)),
        "email": draw(st.emails()),
    }


@given(users())
def test_user_serialization_roundtrip(user):
    assert json.loads(json.dumps(user)) == user


# Stateful testing: exercise a stack and check an invariant after each command
class StackMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.items = []

    @rule(x=st.integers())
    def push(self, x):
        self.items.append(x)

    @precondition(lambda self: len(self.items) > 0)
    @rule()
    def pop(self):
        self.items.pop()

    @invariant()
    def size_is_never_negative(self):
        assert len(self.items) >= 0


TestStack = StackMachine.TestCase
