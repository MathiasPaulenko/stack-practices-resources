# Fine-Tune and Deploy Text Classifiers — Companion Files

Runnable examples for the recipe
[Fine-Tune and Deploy Text Classifiers with Hugging Face](https://stackpractices.com/recipes/python-huggingface-text-classification/).

## Files

- `train.py` — end-to-end training: loads a 2k IMDb subset, tokenizes with `AutoTokenizer`, fine-tunes `distilbert-base-uncased` via `Trainer` (F1 + accuracy), and saves the best checkpoint plus tokenizer to `./sentiment-classifier`.
- `infer.py` — `TextClassificationService` that wraps `pipeline` for batch predictions with human-readable labels.
- `requirements.txt` — `transformers`, `datasets`, `evaluate`, `torch`, `accelerate`.

## Usage

```bash
pip install -r requirements.txt
python train.py   # ~5-10 min on a T4 GPU, ~30-60 min on CPU
python infer.py
```

A GPU is recommended but not required — the IMDb subset is small enough to train on CPU.
