"""Stateful testing with RuleBasedStateMachine.

Companion code for https://stackpractices.com/recipes/python-hypothesis-property-testing/

Usage:
    pytest test_stateful.py -v
"""

from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule


class StackMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.stack = []

    @rule(value=st.integers())
    def push(self, value):
        self.stack.append(value)

    @rule()
    def pop(self):
        if self.stack:
            self.stack.pop()

    @invariant()
    def stack_size_non_negative(self):
        assert len(self.stack) >= 0


TestStack = StackMachine.TestCase
