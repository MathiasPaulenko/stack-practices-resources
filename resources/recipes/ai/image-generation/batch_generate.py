"""Batch image-generation prompt renderer with cache-key hashing.

Renders the prompt templates from prompt_templates.json for a given theme,
computes the cache key (prompt + model + seed) used to dedupe generations,
and prints a dry-run plan. Pass --call-api to actually call the OpenAI
Images API (requires the openai package and OPENAI_API_KEY).

Usage:
    python batch_generate.py "wireless headphones"            # dry run
    python batch_generate.py "wireless headphones" --call-api # real calls
"""

import argparse
import hashlib
import json
from pathlib import Path

MODEL = "dall-e-3"
SEED = 42


def load_templates(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def cache_key(prompt: str, model: str = MODEL, seed: int = SEED) -> str:
    """Stable dedupe key for a generation request."""
    return hashlib.sha256(f"{model}|{seed}|{prompt}".encode()).hexdigest()[:16]


def render(templates: list[dict], theme: str) -> list[dict]:
    plan = []
    for t in templates:
        prompt = t["prompt"].replace("{theme}", theme)
        plan.append(
            {
                "category": t["category"],
                "size": t["size"],
                "prompt": prompt,
                "cache_key": cache_key(prompt),
                "filename": f"{theme.replace(' ', '_')}_{t['category']}.png",
            }
        )
    return plan


def call_openai(plan: list[dict], output_dir: Path) -> None:
    """Execute the plan against the OpenAI Images API."""
    import requests
    from openai import OpenAI

    client = OpenAI()
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in plan:
        response = client.images.generate(
            model=MODEL, prompt=item["prompt"], size=item["size"], n=1
        )
        url = response.data[0].url
        (output_dir / item["filename"]).write_bytes(requests.get(url).content)
        print(f"saved {item['filename']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("theme", help="subject inserted into each template")
    parser.add_argument("--call-api", action="store_true")
    parser.add_argument("--out", default="generated")
    args = parser.parse_args()

    templates = load_templates(Path(__file__).with_name("prompt_templates.json"))
    plan = render(templates, args.theme)

    if args.call_api:
        call_openai(plan, Path(args.out))
    else:
        print(f"Dry run — {len(plan)} images would be generated:")
        for item in plan:
            print(f"  [{item['cache_key']}] {item['filename']} ({item['size']})")
            print(f"      {item['prompt']}")
