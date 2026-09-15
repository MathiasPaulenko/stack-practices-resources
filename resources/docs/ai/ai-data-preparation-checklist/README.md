# AI Data Preparation Checklist — Companion Scripts

Scripts for preparing data for LLM and RAG systems, accompanying the
[AI Data Preparation Checklist](https://stackpractices.com/docs/ai-data-preparation-checklist/).

## Files

| File | Purpose |
|------|---------|
| `clean_text.py` | Remove HTML, normalize whitespace, strip boilerplate |
| `detect_pii.py` | Detect and redact PII (email, phone, SSN, credit card, IP) |
| `find_duplicates.py` | Exact and near-duplicate detection with TF-IDF cosine similarity |
| `chunk_documents.py` | Split documents into chunks with metadata using LangChain |
| `generate_embeddings.py` | Generate embeddings in batches with rate limiting |
| `test_retrieval.py` | Test retrieval quality with hit-rate metric |

## Requirements

```bash
pip install scikit-learn langchain openai
```

Set the `OPENAI_API_KEY` environment variable before running
`generate_embeddings.py`.

## Usage

Each script is standalone and runnable. Run any script directly to see a
demo with sample data:

```bash
python clean_text.py
python detect_pii.py
python find_duplicates.py
python chunk_documents.py
python test_retrieval.py
```

For `generate_embeddings.py`, provide your own chunks and set the API key.
