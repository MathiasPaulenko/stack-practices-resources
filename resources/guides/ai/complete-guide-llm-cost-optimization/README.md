# LLM Cost Optimization — Companion

Runnable toolkit from [Complete Guide to LLM Cost Optimization](https://stackpractices.com/guides/complete-guide-llm-cost-optimization/).

| File | Description |
|------|-------------|
| `router.py` | `ModelRouter` + `CascadingRouter` (cheap-first, escalate on UNCERTAIN) |
| `cache.py` | `LLMCache` exact-match + `SemanticCache` |
| `budget.py` | `BudgetController` — soft alert at 80%, hard stop at 100% |
| `batch_job.py` | OpenAI Batch API helpers (50% off, 24h) |
| `token_counter.py` | `TokenManager` with tiktoken |
| `test_cost.py` | Offline unit tests |
| `requirements.txt` | Pinned deps |

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
pytest test_cost.py -v   # runs fully offline
```
