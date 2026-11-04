"""Regression test suite for LLM apps — dataset built from prod failures."""
import json
from dataclasses import dataclass


@dataclass
class TestCase:
    id: str
    input: str
    expected_output: str
    min_score: float
    category: str


class LLMTestSuite:
    def __init__(self, test_file: str):
        self.tests: list[TestCase] = []
        with open(test_file) as f:
            for item in json.load(f)["tests"]:
                self.tests.append(TestCase(**item))

    def run(self, llm_fn, judge_fn=None) -> dict:
        results = []
        for test in self.tests:
            output = llm_fn(test.input)
            score = judge_fn(test.input, output, test.expected_output) if judge_fn \
                else self._similarity(output, test.expected_output)
            results.append({
                "id": test.id, "category": test.category, "score": score,
                "passed": score >= test.min_score,
                "input": test.input, "output": output[:200],
                "expected": test.expected_output[:200],
            })
        passed = sum(1 for r in results if r["passed"])
        return {"total": len(results), "passed": passed,
                "failed": len(results) - passed,
                "pass_rate": passed / len(results) if results else 0,
                "results": results}

    @staticmethod
    def _similarity(a: str, b: str) -> float:
        wa, wb = set(a.lower().split()), set(b.lower().split())
        if not wa or not wb:
            return 0.0
        return len(wa & wb) / len(wa | wb)
