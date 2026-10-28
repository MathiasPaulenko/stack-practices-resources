# Cache Strategy Decision Template — Companion

Companion to the StackPractices doc [Cache Strategy Decision Template](https://stackpractices.com/docs/cache-strategy-decision-template/).

## Files

| File | Run |
| --- | --- |
| `src/decision_generator.py` | `python src/decision_generator.py` |

An interactive CLI (Python stdlib only) that walks the same questions as the doc's decision tree — data churn rate, write share, loss tolerance, predictable access, write consistency — recommends a strategy (no-cache / cache-aside / read-through / write-through / write-back / refresh-ahead) and prints a filled **Cache Strategy Decision Record** ready to paste into service docs or an ADR.
