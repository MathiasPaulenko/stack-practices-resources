"""Golden-dataset evaluation harness for prompt changes.

Runs tests.json cases against a prompt builder and gates on pass rate.
Works offline with --dry-run (no API calls).

Usage:
    python eval_harness.py --dry-run    # validate dataset + wiring, no API
    python eval_harness.py              # real run, needs OPENAI_API_KEY
"""
import argparse
import json
import sys
from pathlib import Path

DATASET_PATH = Path(__file__).with_name("tests.json")


def build_prompt(case: dict) -> str:
    """The prompt under test - version this like code."""
    return (
        "Classify the sentiment of this review as exactly one of: "
        "positive, negative, neutral.\n\n"
        f'Review: "{case["input"]}"\nSentiment:'
    )


def extract_answer(raw: str) -> str:
    return raw.strip().lower().rstrip(".")


def run(client=None) -> dict:
    cases = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    results = []
    for case in cases:
        if client is None:
            output = case["expected"]  # dry-run: exercise pipeline only
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.0,
                messages=[{"role": "user", "content": build_prompt(case)}],
            )
            output = response.choices[0].message.content
        results.append(
            {
                "id": case["id"],
                "expected": case["expected"],
                "predicted": extract_answer(output),
                "pass": extract_answer(output) == case["expected"],
            }
        )
    passed = sum(r["pass"] for r in results)
    return {"total": len(results), "passed": passed, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="no API calls")
    parser.add_argument("--min-pass-rate", type=float, default=0.9)
    args = parser.parse_args()

    client = None
    if not args.dry_run:
        from openai import OpenAI

        client = OpenAI()

    report = run(client)
    rate = report["passed"] / report["total"]
    print(f"{report['passed']}/{report['total']} passed ({rate:.0%})")
    for r in report["results"]:
        if not r["pass"]:
            print(f"  FAIL {r['id']}: expected={r['expected']} predicted={r['predicted']}")
    return 0 if rate >= args.min_pass_rate else 1


if __name__ == "__main__":
    sys.exit(main())
