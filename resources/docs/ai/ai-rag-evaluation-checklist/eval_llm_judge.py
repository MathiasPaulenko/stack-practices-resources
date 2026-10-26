"""Custom LLM-as-judge evaluator for RAG responses.

Scores each test item on faithfulness, relevance and correctness (1-5)
using a judge model, then prints aggregate averages. Keep temperature=0
so scores are stable enough for regression comparison.

Usage:
    pip install openai
    export OPENAI_API_KEY=...
    python eval_llm_judge.py
"""

import json
import os

from openai import OpenAI

client = OpenAI()

# Replace with records captured from your RAG pipeline.
TEST_SET = [
    {
        "query": "What is the refund policy?",
        "chunks": [
            "Refunds are available within 30 days of purchase. "
            "Contact support with your order number to start a return."
        ],
        "answer": "Customers can request refunds within 30 days of purchase.",
        "ground_truth": "Refunds are available within 30 days.",
    }
]


def evaluate_rag_response(query, retrieved_chunks, answer, ground_truth):
    eval_prompt = f"""
Evaluate this RAG response on three criteria. Score each 1-5.

Query: {query}
Retrieved context: {retrieved_chunks}
Generated answer: {answer}
Ground truth: {ground_truth}

Criteria:
1. Faithfulness: Is every claim in the answer supported by the context?
2. Relevance: Does the answer directly address the query?
3. Correctness: Does the answer match the ground truth?

Return JSON: {{"faithfulness": N, "relevance": N, "correctness": N}}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)


def main() -> None:
    results = [
        evaluate_rag_response(
            item["query"], item["chunks"], item["answer"], item["ground_truth"]
        )
        for item in TEST_SET
    ]
    for key in ("faithfulness", "relevance", "correctness"):
        avg = sum(r[key] for r in results) / len(results)
        print(f"{key.capitalize()}: {avg:.2f}")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY before running.")
    main()
