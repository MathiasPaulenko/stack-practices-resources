"""Prompt evaluation script for the AI Prompt Version Control Template.

Runs a prompt version against a fixed test set and reports accuracy.
Usage:
    python eval_prompt.py --prompt prompts/classifier/prompt.md \
        --test-set prompts/classifier/eval/test_set.jsonl \
        --model gpt-4o-mini --threshold 0.88
"""
import argparse
import json
from openai import OpenAI

client = OpenAI()


def evaluate_prompt_version(prompt_path: str, test_set_path: str, model: str) -> dict:
    with open(prompt_path) as f:
        prompt_template = f.read()

    with open(test_set_path) as f:
        test_cases = [json.loads(line) for line in f]

    correct = 0
    total = len(test_cases)

    for case in test_cases:
        prompt = prompt_template.replace("{{input_text}}", case["input"])
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        prediction = response.choices[0].message.content.strip()

        if prediction == case["expected"]:
            correct += 1

    accuracy = correct / total

    return {
        "version": prompt_path.split("/")[-1].replace(".md", ""),
        "accuracy": accuracy,
        "test_cases": total,
        "correct": correct,
        "incorrect": total - correct,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a prompt version")
    parser.add_argument("--prompt", required=True, help="Path to the prompt file")
    parser.add_argument("--test-set", required=True, help="Path to the JSONL test set")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to use")
    parser.add_argument("--threshold", type=float, default=0.88, help="Min accuracy")
    args = parser.parse_args()

    results = evaluate_prompt_version(args.prompt, args.test_set, args.model)
    print(json.dumps(results, indent=2))

    if results["accuracy"] < args.threshold:
        raise SystemExit(
            f"FAIL: accuracy {results['accuracy']} below threshold {args.threshold}"
        )
    print(f"PASS: accuracy {results['accuracy']} meets threshold {args.threshold}")


if __name__ == "__main__":
    main()
