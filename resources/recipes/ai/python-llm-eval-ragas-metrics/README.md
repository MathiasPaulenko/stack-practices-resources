# Evaluate RAG Quality with RAGAS Metrics

Runnable companion for the StackPractices recipe:
<https://stackpractices.com/recipes/python-llm-eval-ragas-metrics/>

## Files

- `eval_rag.py` — complete evaluation runner: sample dataset in the RAGAS 0.2+ schema (`user_input`/`response`/`retrieved_contexts`/`reference`), four core metrics, formatted report printer, `evaluate_rag_pipeline` for your own RAG, and `evaluate_from_csv` for batch runs.

## Requirements

```bash
pip install ragas langchain-openai datasets pandas
export OPENAI_API_KEY=...   # evaluator LLM + embeddings
```

## Run

```bash
python eval_rag.py
```

## Notes

- The examples target **RAGAS 0.2+**. If your code uses `question`/`answer`/`contexts`/`ground_truth`, rename the columns or pin `ragas<0.2`.
- Pin your evaluator model per project — scores from different judge models aren't comparable.
- Context recall needs `reference` answers; without them you only get three of the four metrics.
