"""Batch inference service for the fine-tuned text classifier.

Companion code for https://stackpractices.com/recipes/python-huggingface-text-classification/

Run train.py first to produce ./sentiment-classifier.
"""

from typing import List

import torch
from transformers import pipeline


class TextClassificationService:
    def __init__(self, model_dir: str):
        self.classifier = pipeline(
            "text-classification",
            model=model_dir,
            tokenizer=model_dir,
            device=0 if torch.cuda.is_available() else -1,
        )
        self.label_map = {0: "negative", 1: "positive"}

    def classify(self, texts: List[str]) -> List[dict]:
        """Classify a batch of texts.

        Args:
            texts: List of input texts.

        Returns:
            List of {label, score, text} dicts.
        """
        results = self.classifier(texts, batch_size=32)
        return [
            {
                "label": self.label_map.get(
                    int(r["label"].split("_")[-1]), r["label"]
                ),
                "score": r["score"],
                "text": text[:100],
            }
            for r, text in zip(results, texts)
        ]


if __name__ == "__main__":
    service = TextClassificationService("./sentiment-classifier")
    predictions = service.classify(
        [
            "Great product, highly recommend!",
            "Terrible experience, would not buy again.",
            "It's okay, nothing special.",
        ]
    )
    for p in predictions:
        print(f"{p['label']}: {p['score']:.3f} — {p['text']}")
