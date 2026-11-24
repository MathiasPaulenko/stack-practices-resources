"""Fine-tune DistilBERT for text classification with Hugging Face Trainer.

Companion code for https://stackpractices.com/recipes/python-huggingface-text-classification/

Requirements:
    pip install -r requirements.txt

Usage:
    python train.py            # trains on a 2k IMDb subset, saves ./sentiment-classifier
    python infer.py            # batch inference with the saved model
"""

import evaluate
import torch
from datasets import DatasetDict, load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilbert-base-uncased"
MODEL_DIR = "./sentiment-classifier"


def load_imdb_subset(train_size=2000, test_size=500):
    dataset = load_dataset("imdb")
    return DatasetDict(
        {
            "train": dataset["train"].shuffle(seed=42).select(range(train_size)),
            "test": dataset["test"].shuffle(seed=42).select(range(test_size)),
        }
    )


def tokenize(dataset, tokenizer, max_length=256):
    def _fn(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )

    tokenized = dataset.map(_fn, batched=True)
    tokenized.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    return tokenized


def build_compute_metrics():
    f1_metric = evaluate.load("f1")
    accuracy_metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = logits.argmax(axis=-1)
        return {
            "f1": f1_metric.compute(predictions=predictions, references=labels)["f1"],
            "accuracy": accuracy_metric.compute(
                predictions=predictions, references=labels
            )["accuracy"],
        }

    return compute_metrics


def main():
    dataset = load_imdb_subset()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenized = tokenize(dataset, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=2
    )

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=100,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_dir="./logs",
        logging_steps=50,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        compute_metrics=build_compute_metrics(),
    )

    trainer.train()
    print(trainer.evaluate())

    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
    print(f"Saved to {MODEL_DIR} (cuda={torch.cuda.is_available()})")


if __name__ == "__main__":
    main()
