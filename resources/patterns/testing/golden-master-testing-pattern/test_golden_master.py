"""Verify refactored calculator matches the golden master."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


def load_golden_master():
    with open(Path(__file__).parent / "golden_master.json") as f:
        return json.load(f)


def run_refactored_system(input_data):
    """Run the refactored system."""
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "refactored_calculator.py")],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
    )
    return result.stdout


@pytest.mark.parametrize("case", load_golden_master())
def test_matches_golden_master(case):
    input_data = case["input"]
    expected_hash = case["hash"]
    actual_output = run_refactored_system(input_data)
    actual_hash = hashlib.sha256(actual_output.encode()).hexdigest()
    assert actual_hash == expected_hash, (
        f"Output mismatch for input: {input_data}\n"
        f"Expected hash: {expected_hash}\n"
        f"Actual hash:   {actual_hash}"
    )
