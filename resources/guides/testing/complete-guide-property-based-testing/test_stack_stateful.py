# Stateful property testing with RuleBasedStateMachine.
# Run: pytest test_stack_stateful.py -v
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from hypothesis import strategies as st

class StackMachine(RuleBasedStateMachine):
    """Random sequences of push/pop; invariants checked after every step."""

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
