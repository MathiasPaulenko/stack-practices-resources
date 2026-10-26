# AI RAG Evaluation Checklist — Companion Scripts

Runnable scripts for evaluating RAG system quality, accompanying the
[AI RAG Evaluation Checklist](https://stackpractices.com/docs/ai-rag-evaluation-checklist/).

## Files

| File | Purpose |
|------|---------|
| `eval_ragas.py` | RAGAS metrics: faithfulness, answer relevancy, context precision and recall |
| `eval_llm_judge.py` | Custom LLM-as-judge scoring (faithfulness, relevance, correctness) for regression gates |
| `requirements.txt` | Python dependencies |

## Requirements

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
```

RAGAS uses an LLM internally for several metrics, so `OPENAI_API_KEY`
(or a configured alternative LLM) is required for both scripts.

## Usage

```bash
python eval_ragas.py
python eval_llm_judge.py
```

Both scripts ship with two small sample records. Replace `SAMPLES` /
`TEST_SET` with real query-answer-context-ground_truth tuples captured
from your pipeline — 50+ items is the minimum for a meaningful score.

Suggested thresholds before sign-off (see the checklist doc):

- Context precision > 0.75 at k=5
- Context recall > 0.80 at k=10
- Faithfulness > 0.90
- Answer correctness > 0.85
