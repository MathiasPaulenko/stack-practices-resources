"""RAGAS evaluation for RAG pipelines. pip install ragas datasets
API varies by version — this follows ragas>=0.1."""
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)


def run_ragas_eval(eval_data: dict) -> dict:
    """Evaluate a question/answer/contexts/ground_truth dict with RAGAS."""
    dataset = Dataset.from_dict(eval_data)
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    )
    return dict(results)


if __name__ == "__main__":
    data = {
        "question": ["What is Python's GIL?"],
        "answer": ["The GIL is a mutex that protects access to Python objects."],
        "contexts": [["Python's GIL (Global Interpreter Lock) is a mutex that prevents "
                      "multiple threads from executing Python bytecodes at once."]],
        "ground_truth": ["The GIL is a mutex that prevents multiple native threads "
                         "from executing Python bytecodes simultaneously."],
    }
    print(run_ragas_eval(data))
