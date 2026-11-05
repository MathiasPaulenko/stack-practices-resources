"""RAGAS evaluation for RAG pipelines.

A RAG system has four places to fail independently: parsing can mangle
documents, retrieval can miss the right chunk, the reranker can demote it,
and the LLM can ignore or distort what it was given. RAGAS measures the
second half (generation given retrieved context) with four metrics:

    faithfulness        — is every claim supported by the retrieved context?
    answer_relevancy    — does the answer address the question asked?
    context_precision   — are the retrieved chunks relevant?
    context_recall      — did retrieval fetch everything needed?

Two practical notes:

- contexts must be the chunks YOUR retriever actually returned, not ideal
  answers — evaluating against ideal contexts measures a pipeline you
  don't have.
- RAGAS scores are themselves LLM-judged, so they inherit judge noise: run
  enough samples (50+) before trusting a delta, and prefer relative
  comparisons between versions over absolute scores.

Requires an LLM configured for ragas (e.g. OPENAI_API_KEY). API varies by
ragas version — this follows the classic ragas.metrics API; newer versions
expose a collections-based API in the docs (check latest docs).
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional

def _load_metrics():
    from ragas.metrics import (
        answer_relevancy,
        context_precision,
        context_recall,
        faithfulness,
    )

    return [faithfulness, answer_relevancy, context_precision, context_recall]


def load_eval_dataset(path: str = "tests.json") -> Dict[str, list]:
    """Load a RAGAS-shaped dataset: question/answer/contexts/ground_truth."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"question", "answer", "contexts", "ground_truth"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"Eval dataset missing keys: {sorted(missing)}")
    return data


def run_ragas_eval(
    eval_data: Dict[str, list],
    metrics: Optional[List[Any]] = None,
    llm: Any = None,
    embeddings: Any = None,
) -> Dict[str, float]:
    """Evaluate a question/answer/contexts/ground_truth dataset with RAGAS.

    eval_data["contexts"] must be a list (one per row) of lists of retrieved
    chunk strings — the actual retriever output. Pass llm=/embeddings= for
    ragas versions that require explicit clients.
    """
    from datasets import Dataset
    from ragas import evaluate

    dataset = Dataset.from_dict(eval_data)
    kwargs: Dict[str, Any] = {"metrics": metrics if metrics is not None else _load_metrics()}
    if llm is not None:
        kwargs["llm"] = llm
    if embeddings is not None:
        kwargs["embeddings"] = embeddings

    results = evaluate(dataset, **kwargs)
    return dict(results)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    dataset_path = here / "tests.json"
    eval_data = load_eval_dataset(str(dataset_path)) if dataset_path.exists() else {
        "question": ["How do I configure SSO for the admin panel?"],
        "answer": ["SSO is configured under Admin > Security > Identity providers."],
        "contexts": [["Admin > Security > Identity providers lets you connect SAML or OIDC..."]],
        "ground_truth": ["SSO setup is done in Admin > Security > Identity providers via SAML/OIDC."],
    }
    # Needs an LLM for ragas — set OPENAI_API_KEY (or pass llm= to run_ragas_eval).
    print(run_ragas_eval(eval_data))
