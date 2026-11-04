# Complete Guide to LLM Prompt Engineering - Code Examples

Runnable examples from the guide:
<https://stackpractices.com/guides/complete-guide-llm-prompt-engineering/>

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Files

| File | What it shows |
| --- | --- |
| `prompts.py` | System prompt contracts + untrusted-content delimiters |
| `few_shot.py` | Zero-shot vs few-shot classification |
| `self_consistency.py` | Majority-vote CoT sampling (n=5) |
| `structured_output.py` | JSON mode + Pydantic validation + repair retry |
| `rag_grounding.py` | Embed-once index + grounded answering |
| `function_calling.py` | Two-step tool loop with parallel call handling |
| `eval_harness.py` | Golden-dataset regression gate for prompt changes |
| `tests.json` | Golden dataset used by the harness |

## Offline check

```bash
python eval_harness.py --dry-run
```

Validates the dataset and wiring without API calls. Real runs need
`OPENAI_API_KEY` and a few cents of `gpt-4o-mini` usage.
