"""Static attack-corpus harness: run attack strings through the defense
layers and report what each layer caught - no API calls needed.

Usage:
    python security_harness.py            # run the corpus
    python security_harness.py --verbose  # show per-attack details
"""
import argparse
import json
import sys
from pathlib import Path

from injection_guard import PromptInjectionGuard
from document_sanitizer import DocumentSanitizer
from jailbreak_detector import JailbreakDetector

CORPUS_PATH = Path(__file__).with_name("attack_corpus.json")


def run(verbose: bool = False) -> dict:
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    guard = PromptInjectionGuard()
    sanitizer = DocumentSanitizer()
    jb = JailbreakDetector()

    results = []
    for case in corpus:
        injection_hit = not guard.check(case["input"])[0]
        jb_hit = jb.detect(case["input"]).get("is_jailbreak", False)
        sanitized_changed = sanitizer.sanitize(case["input"]) != case["input"]
        detected = injection_hit or jb_hit or sanitized_changed
        expected = case.get("should_detect", True)
        results.append(
            {
                "id": case["id"],
                "expected_detect": expected,
                "injection_hit": injection_hit,
                "jailbreak_hit": jb_hit,
                "sanitized": sanitized_changed,
                "pass": detected == expected,
            }
        )
        if verbose:
            print(json.dumps(results[-1]))

    passed = sum(r["pass"] for r in results)
    return {"total": len(results), "passed": passed, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    report = run(verbose=args.verbose)
    rate = report["passed"] / report["total"]
    print(f"{report['passed']}/{report['total']} expected outcomes ({rate:.0%})")
    for r in report["results"]:
        if not r["pass"]:
            print(f"  MISS {r['id']}: expected detect={r['expected_detect']}")
    return 0 if rate >= 0.9 else 1


if __name__ == "__main__":
    sys.exit(main())
