"""RAGAS evaluation runner for RAG pipelines.

Companion to https://stackpractices.com/recipes/python-llm-eval-ragas-metrics/
Targets the RAGAS 0.2+ dataset schema (user_input / response /
retrieved_contexts / reference).

Requires: pip install ragas langchain-openai datasets pandas
Set OPENAI_API_KEY before running.
"""

import pandas as pd
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

METRICS = [faithfulness, answer_relevancy, context_precision, context_recall]


def build_eval_dataset() -> Dataset:
    """Sample evaluation dataset in the RAGAS 0.2+ schema."""
    eval_data = {
        "user_input": [
            "What is the Redis cache-aside pattern?",
            "How does Docker Compose define multi-container apps?",
            "What are PostgreSQL ACID compliance features?",
        ],
        "response": [
            "The cache-aside pattern checks the cache first, and if data is missing, loads it from the database and sets it in the cache with a TTL.",
            "Docker Compose uses a YAML file to define multi-container applications, specifying services, networks, and volumes.",
            "PostgreSQL provides ACID compliance through atomic transactions, consistent constraints, isolation levels, and durable write-ahead logging.",
        ],
        "retrieved_contexts": [
            ["Redis cache-aside: application checks cache first. On cache miss, loads from database and sets cache entry with TTL."],
            ["Docker Compose is a tool for defining multi-container Docker applications in a YAML file with services, networks, and volumes."],
            ["PostgreSQL ensures ACID compliance: atomicity via transactions, consistency via constraints, isolation via MVCC, durability via WAL."],
        ],
        "reference": [
            "Cache-aside checks cache first, loads from DB on miss, sets cache with TTL.",
            "Docker Compose defines multi-container apps in YAML with services, networks, and volumes.",
            "PostgreSQL ACID: atomicity (transactions), consistency (constraints), isolation (MVCC), durability (WAL).",
        ],
    }
    return Dataset.from_dict(eval_data)


def run_evaluation(dataset: Dataset, eval_llm=None, eval_embeddings=None):
    """Run RAGAS with the four core metrics."""
    eval_llm = eval_llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
    eval_embeddings = eval_embeddings or OpenAIEmbeddings(model="text-embedding-3-small")
    return evaluate(dataset, metrics=METRICS, llm=eval_llm, embeddings=eval_embeddings)


def print_eval_report(results) -> None:
    """Print a formatted evaluation report."""
    df = results.to_pandas()

    print("=" * 60)
    print("RAGAS Evaluation Report")
    print("=" * 60)

    metric_names = [m.name for m in METRICS]
    for metric in metric_names:
        scores = df[metric].tolist()
        avg = sum(scores) / len(scores)
        print(f"\n{metric.replace('_', ' ').title()}:")
        print(f"  Average: {avg:.3f}")
        print(f"  Min:     {min(scores):.3f}")
        print(f"  Max:     {max(scores):.3f}")
        for i, score in enumerate(scores):
            print(f"  Q{i+1}: {score:.3f}")

    aggregate = sum(df[m].mean() for m in metric_names) / len(metric_names)
    print("\n" + "=" * 60)
    print(f"Aggregate Score: {aggregate:.3f}")


def evaluate_rag_pipeline(rag_pipeline, test_cases: list[dict], **kwargs):
    """Evaluate a RAG pipeline exposing .ask(query) -> {answer, sources}.

    test_cases: list of {question, ground_truth} dicts.
    """
    eval_rows = []
    for case in test_cases:
        result = rag_pipeline.ask(case["question"])
        eval_rows.append({
            "user_input": case["question"],
            "response": result["answer"],
            "retrieved_contexts": [s["text"] for s in result["sources"]],
            "reference": case["ground_truth"],
        })

    dataset = Dataset.from_list(eval_rows)
    return evaluate(dataset, metrics=METRICS, **kwargs)


def evaluate_from_csv(csv_path: str, **kwargs) -> pd.DataFrame:
    """Load test cases from CSV and evaluate.

    CSV columns: question, answer, contexts (semicolon-separated), ground_truth.
    """
    df = pd.read_csv(csv_path)
    eval_data = {
        "user_input": df["question"].tolist(),
        "response": df["answer"].tolist(),
        "retrieved_contexts": [c.split(";") for c in df["contexts"]],
        "reference": df["ground_truth"].tolist(),
    }
    dataset = Dataset.from_dict(eval_data)
    return evaluate(dataset, metrics=METRICS, **kwargs).to_pandas()


if __name__ == "__main__":
    results = run_evaluation(build_eval_dataset())
    print_eval_report(results)
