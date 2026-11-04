"""Offline decision harness: map query shapes from queries.json to the
index type the guide recommends - no MongoDB required.

Usage: python decide_index.py [--verbose]
"""
import argparse
import json
import sys
from pathlib import Path

QUERIES_PATH = Path(__file__).with_name("queries.json")


def decide(q: dict) -> str:
    """Return the recommended index type for a query shape."""
    if q.get("geo"):
        return "2dsphere"
    if q.get("ttl"):
        return "ttl"
    if q.get("shard_key_even"):
        return "hashed"
    if q.get("dynamic_schema"):
        return "wildcard"
    if q.get("text_search"):
        return "atlas_search" if q.get("needs_fuzzy") else "text"
    if q.get("partial"):
        return "partial"
    if q.get("covers_projection"):
        return "compound (covered)"
    if q.get("sort") and q.get("equality"):
        return "compound (ESR)"
    if q.get("equality") or q.get("range"):
        return "compound"
    return "single field"


def run(verbose: bool = False) -> dict:
    cases = json.loads(QUERIES_PATH.read_text(encoding="utf-8"))
    results = []
    for case in cases:
        got = decide(case["query"])
        expected = case["expected_index"]
        ok = got == expected
        results.append({"id": case["id"], "expected": expected, "got": got, "pass": ok})
        if verbose:
            mark = "OK " if ok else "MISS"
            print(f"{mark} {case['id']}: expected={expected} got={got}")
    return {"total": len(results), "passed": sum(r["pass"] for r in results), "results": results}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    report = run(verbose=args.verbose)
    rate = report["passed"] / report["total"]
    print(f"{report['passed']}/{report['total']} decisions correct ({rate:.0%})")
    return 0 if rate == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
