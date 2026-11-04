"""Offline unit tests — no API calls needed. Run: pytest test_eval.py -v"""
import json

from ab_test import ABTestConfig, ABTestRunner, ab_test_significance, cohen_kappa
from regression_suite import LLMTestSuite


def test_similarity_scores(tmp_path):
    f = tmp_path / "tests.json"
    f.write_text(json.dumps({"tests": [
        {"id": "t1", "input": "2+2?", "expected_output": "4", "min_score": 0.5, "category": "math"}
    ]}))
    suite = LLMTestSuite(str(f))
    report = suite.run(lambda x: "4")
    assert report["pass_rate"] == 1.0


def test_ab_significance():
    r = ab_test_significance(120, 200, 145, 200)
    assert r["significant"] and r["rate_b"] > r["rate_a"]
    r2 = ab_test_significance(100, 200, 102, 200)
    assert not r2["significant"]


def test_deterministic_assignment():
    t = ABTestRunner(ABTestConfig("a", "b", 0.5))
    assert t.assign("user-1") == t.assign("user-1")


def test_kappa_perfect_and_low():
    assert cohen_kappa([1, 2, 3], [1, 2, 3]) == 1.0
    assert cohen_kappa([1, 1, 1], [3, 3, 3]) < 0.8
