# Compare Text Semantic Similarity with OpenAI Embeddings

Runnable companion code for the StackPractices recipe
[Compare Text Semantic Similarity with OpenAI Embeddings](https://stackpractices.com/recipes/python-openai-embeddings-cosine/).

## Contents

- `similarity_search.py` — embedding helpers (single, batch, retry with
  backoff), cosine similarity functions, `SimilaritySearchIndex`, and
  threshold-based `find_duplicates`.
- `main.py` — demo that compares two texts, searches a small index, prints
  a pairwise similarity matrix, and detects near-duplicates.
- `requirements.txt` — pinned dependencies (`openai`, `numpy`).

## Usage

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```
