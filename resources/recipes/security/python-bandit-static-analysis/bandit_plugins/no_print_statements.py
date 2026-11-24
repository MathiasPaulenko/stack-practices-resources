"""Example Bandit custom test.

Register it through the bandit.plugins entry-point group in your
project's pyproject.toml, then install the project:

    [project.entry-points."bandit.plugins"]
    no_print_statements = "bandit_plugins.no_print_statements:no_print_statements"
"""

import bandit
from bandit.core import test_properties


@test_properties.checks("Call")
def no_print_statements(context):
    if context.call_function_name == "print":
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            text="Print used; review whether a logger is more appropriate.",
            lineno=context.node.lineno,
        )
