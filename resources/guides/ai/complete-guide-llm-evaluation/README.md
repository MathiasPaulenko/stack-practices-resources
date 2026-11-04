# LLM Evaluation — Companion

Runnable eval suite from [Complete Guide to LLM Evaluation](https://stackpractices.com/guides/complete-guide-llm-evaluation/).

## Files

| File | Description |
|------|-------------|
| `judge.py` | Rubric judge + position-randomized pairwise + majority vote |
| `ragas_eval.py` | RAGAS runner for question/answer/context/ground-truth datasets |
| `regression_suite.py` | `LLMTestSuite` — JSON-driven regression cases with Jaccard/judge scoring |
| `ci_gate.py` | Blocking CI gate with per-test failure report |
| `hallucination.py` | Self-consistency check + claim-vs-source verification |
| `ab_test.py` | Deterministic A/B assignment + z-test + Cohen's kappa |
| `test_eval.py` | Offline unit tests — no API key needed |
| `tests.json` | Sample regression dataset |
| `requirements.txt` | Pinned dependencies |

## Quick start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
pytest test_eval.py -v   # runs fully offline
python ragas_eval.py     # needs API key
```
