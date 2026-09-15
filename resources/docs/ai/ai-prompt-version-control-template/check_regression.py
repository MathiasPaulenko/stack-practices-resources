"""Regression check between two prompt evaluation results.

Compares accuracy of the new version against the old version and
returns PASS, WARN, or FAIL based on the configured max drop.
Usage:
    python check_regression.py \
        --old-results prompts/classifier/eval/eval_results_3.1.0.json \
        --new-results eval_output.json \
        --max-drop 0.02
"""
import argparse
import json


def compare_versions(old_results: dict, new_results: dict, max_drop: float = 0.02) -> dict:
    accuracy_delta = new_results["accuracy"] - old_results["accuracy"]

    verdict = "PASS"
    if accuracy_delta < -max_drop:
        verdict = f"FAIL — accuracy dropped more than {max_drop:.0%}"
    elif accuracy_delta < 0:
        verdict = "WARN — accuracy decreased slightly"

    return {
        "old_version": old_results["version"],
        "new_version": new_results["version"],
        "old_accuracy": old_results["accuracy"],
        "new_accuracy": new_results["accuracy"],
        "delta": accuracy_delta,
        "verdict": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check prompt regression")
    parser.add_argument("--old-results", required=True, help="Previous eval JSON")
    parser.add_argument("--new-results", required=True, help="New eval JSON")
    parser.add_argument("--max-drop", type=float, default=0.02, help="Max allowed drop")
    args = parser.parse_args()

    with open(args.old_results) as f:
        old = json.load(f)
    with open(args.new_results) as f:
        new = json.load(f)

    result = compare_versions(old, new, args.max_drop)
    print(json.dumps(result, indent=2))

    if result["verdict"].startswith("FAIL"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
