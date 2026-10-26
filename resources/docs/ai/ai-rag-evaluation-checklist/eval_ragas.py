"""Evaluate a RAG system with RAGAS metrics.

Measures faithfulness, answer relevancy, context precision and context
recall over a small golden test set. Replace `SAMPLES` with real
query/answer/context/ground-truth tuples from your system.

Usage:
    pip install ragas datasets openai
    export OPENAI_API_KEY=...
    python eval_ragas.py
"""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

# Replace with real records captured from your RAG pipeline.
SAMPLES = {
    "question": [
        "What is the refund policy?",
        "How do I reset my password?",
    ],
    "answer": [
        "Customers can request refunds within 30 days of purchase.",
        "Go to Settings > Security and click 'Reset password'.",
    ],
    "contexts": [
        [
            "Refunds are available within 30 days of purchase. "
            "Contact support with your order number to start a return."
        ],
        [
            "To reset your password, open Settings, go to the Security "
            "section and click 'Reset password'. A link is emailed to you."
        ],
    ],
    "ground_truth": [
        "Refunds are available within 30 days.",
        "Reset the password from Settings > Security.",
    ],
}


def main() -> None:
    dataset = Dataset.from_dict(SAMPLES)
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    )
    print(results)
    # Example output:
    # {'faithfulness': 0.92, 'answer_relevancy': 4.2,
    #  'context_precision': 0.85, 'context_recall': 0.88}


if __name__ == "__main__":
    main()
