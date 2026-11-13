# Image Generation — Companion Resources

Runnable helpers for the [image-generation recipe](https://stackpractices.com/recipes/image-generation/).

## Files

- `batch_generate.py` — renders prompt templates for a theme, computes the
  cache key (`model + seed + prompt`) used to dedupe generations, and prints a
  dry-run plan. With `--call-api` it calls the OpenAI Images API for real
  (requires `pip install openai requests` and `OPENAI_API_KEY`).
- `prompt_templates.json` — prompt template set (hero, thumbnail, icon) with
  `{theme}` placeholders and target sizes.

## Run

```bash
python batch_generate.py "wireless headphones"            # dry run, no API key needed
python batch_generate.py "wireless headphones" --call-api # real generation
```

The dry run shows the three prompts that would be sent, the dedupe cache key
for each, and the output filename. Re-running with the same theme produces the
same cache keys, which is how the recipe's cache-by-prompt-hash works.
