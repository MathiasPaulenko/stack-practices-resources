# Apply Prompt Engineering: What Works — Companion Files

Companion resources for the recipe
[Apply Prompt Engineering: What Works](https://stackpractices.com/recipes/prompt-engineering/).

## Contents

| File | Purpose |
|------|---------|
| `prompt-eval-suite.py` | Runs a prompt against a JSON test set and reports pass/fail. Exits non-zero below a threshold — usable as a CI gate for prompt regressions. |
| `few-shot-template.md` | Reusable few-shot prompt skeleton for classification/extraction tasks. |
| `test-set.example.json` | Sample intent-classification test set (10 input/expected pairs). |

## Usage

```bash
pip install openai
export OPENAI_API_KEY=sk-...

python prompt-eval-suite.py \
  --test-set test-set.example.json \
  --system "Classify user intent into: SEARCH, SUPPORT, BILLING, or OTHER." \
  --threshold 0.9
```

Pass rate below the threshold → exit code 1, failures dumped to `eval-failures.json`.

## License

See the repository root `LICENSE`.
