"""Report the unit / integration / e2e distribution of a test suite.

Run from the repository root after organizing tests into
tests/unit, tests/integration and tests/e2e directories:

    python report_test_distribution.py
"""
from pathlib import Path
import re


def count_tests(directory: str, pattern: str) -> int:
    """Count test definitions in files matching pattern under directory."""
    path = Path(directory)
    if not path.exists():
        return 0
    return sum(
        len(re.findall(r'\b(it|test|def test_)\s*\(', f.read_text()))
        for f in path.rglob(pattern)
    )


unit = count_tests('tests/unit', '*.py')
integration = count_tests('tests/integration', '*.py')
e2e = count_tests('tests/e2e', '*.py')
total = unit + integration + e2e or 1

print(f"Unit:        {unit:4} ({unit/total:.0%})")
print(f"Integration: {integration:4} ({integration/total:.0%})")
print(f"E2E:         {e2e:4} ({e2e/total:.0%})")

if e2e / total > 0.15:
    print("\nWARNING: E2E tests exceed 15% — check for ice cream cone")
