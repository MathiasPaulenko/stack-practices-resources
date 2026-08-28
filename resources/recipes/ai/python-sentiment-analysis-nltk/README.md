# Sentiment Analysis with Python and NLTK — Companion Resources

Runnable examples for the [Sentiment Analysis with Python and NLTK](https://stackpractices.com/recipes/python-sentiment-analysis-nltk/) recipe.

## Files

| File | Description |
|------|-------------|
| `sentiment_basic.py` | Basic VADER sentiment scoring |
| `classify_sentiment.py` | Classify text into positive/negative/neutral labels |
| `csv_batch.py` | Batch process sentiment scoring from a CSV file |
| `custom_lexicon.py` | Customize VADER lexicon with domain-specific words |
| `sentiment_over_time.py` | Track sentiment trends over time |
| `requirements.txt` | Python dependencies (nltk) |

## Quick Start

```bash
pip install -r requirements.txt
python sentiment_basic.py
python classify_sentiment.py
python custom_lexicon.py
python sentiment_over_time.py
```

For CSV batch processing, create a `reviews.csv` with a `review` column:

```bash
python csv_batch.py
# Output: scored.csv with sentiment and compound columns
```

## Key Points

- Use the `compound` score for classification (range -1 to +1).
- Default thresholds: +0.05 for positive, -0.05 for negative.
- Customize the lexicon with domain-specific words for better accuracy.
- VADER is English-only; for Spanish use `pysentimiento`.
- Score long documents paragraph by paragraph, not as a whole.
