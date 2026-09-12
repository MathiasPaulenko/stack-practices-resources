"""Generate a golden master from the legacy calculator."""

import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path


def run_legacy_system(input_data):
    """Run the legacy system with given input and capture output."""
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "legacy_calculator.py")],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
    )
    return result.stdout


def generate_test_inputs(count=500):
    """Generate diverse inputs to exercise the legacy system."""
    inputs = []
    for _ in range(count // 2):
        inputs.append({
            "operation": random.choice(["add", "subtract", "multiply", "divide"]),
            "a": random.uniform(-1000, 1000),
            "b": random.uniform(-1000, 1000),
        })
    inputs.extend([
        {"operation": "add", "a": 0, "b": 0},
        {"operation": "divide", "a": 1, "b": 0},
        {"operation": "multiply", "a": -1, "b": -1},
        {"operation": "add", "a": 1e10, "b": -1e10},
        {"operation": "subtract", "a": 0.1, "b": 0.3},
        {"operation": "add", "a": float("inf"), "b": 1},
        {"operation": "add", "a": float("-inf"), "b": 1},
        {"operation": "add", "a": float("nan"), "b": 1},
    ])
    return inputs


def generate_golden_master(output_file="golden_master.json"):
    """Generate golden master from test inputs."""
    inputs = generate_test_inputs()
    outputs = []
    for input_data in inputs:
        output = run_legacy_system(input_data)
        outputs.append({
            "input": input_data,
            "output": output,
            "hash": hashlib.sha256(output.encode()).hexdigest(),
        })
    with open(output_file, "w") as f:
        json.dump(outputs, f, indent=2)
    print(f"Golden master generated with {len(outputs)} cases -> {output_file}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "golden_master.json"
    generate_golden_master(output)
