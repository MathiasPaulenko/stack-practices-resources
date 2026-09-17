#!/usr/bin/env python3
"""Prompt evaluation suite.

Runs a prompt against a JSON test set and reports pass/fail rates.
Use it before and after any prompt change to catch regressions.

Usage:
    export OPENAI_API_KEY=...
    python prompt-eval-suite.py --test-set test-set.example.json \
        --system "Classify user intent into: SEARCH, SUPPORT, BILLING, or OTHER."

Test set format (JSON array):
    [
      {"input": "How do I reset my password?", "expected": "SUPPORT"},
      {"input": "Find me red shoes under $100", "expected": "SEARCH"}
    ]

Exit code is 0 when the pass rate meets --threshold (default 0.9),
so the script can gate a CI pipeline on prompt regressions.
"""

import argparse
import json
import os
import sys
import time


def run_prompt(client, model: str, system: str, user_input: str) -> str:
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_input},
        ],
    )
    return response.choices[0].message.content.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-set", required=True, help="JSON file with input/expected pairs")
    parser.add_argument("--system", required=True, help="System prompt under test")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--threshold", type=float, default=0.9)
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between calls")
    args = parser.parse_args()

    try:
        import openai
    except ImportError:
        sys.exit("pip install openai")

    client = openai.OpenAI()  # reads OPENAI_API_KEY

    with open(args.test_set, encoding="utf-8") as f:
        cases = json.load(f)

    passed = failed = 0
    failures = []
    for case in cases:
        try:
            got = run_prompt(client, args.model, args.system, case["input"])
        except Exception as exc:  # rate limits, network errors
            print(f"ERROR on {case['input']!r}: {exc}")
            failed += 1
            failures.append(case)
            time.sleep(args.delay * 10)
            continue
        ok = got == case["expected"]
        passed += ok
        failed += not ok
        if not ok:
            failures.append({**case, "got": got})
            print(f"FAIL  input={case['input']!r} expected={case['expected']!r} got={got!r}")
        else:
            print(f"PASS  input={case['input']!r}")
        time.sleep(args.delay)

    total = passed + failed
    rate = passed / total if total else 0.0
    print(f"\n{passed}/{total} passed ({rate:.0%}), threshold {args.threshold:.0%}")

    if failures:
        with open("eval-failures.json", "w", encoding="utf-8") as f:
            json.dump(failures, f, indent=2, ensure_ascii=False)
        print("Failures written to eval-failures.json")

    return 0 if rate >= args.threshold else 1


if __name__ == "__main__":
    sys.exit(main())
