"""Fine-tune a causal language model with LoRA/QLoRA for code generation.

Example (smoke test on CPU with a small model):
    python fine_tune.py \
        --model_name Salesforce/codegen-350M-mono \
        --train_file data/train.jsonl \
        --val_file data/val.jsonl \
        --output_dir ./smoke-lora \
        --num_train_epochs 1 \
        --lora_r 8 \
        --lora_alpha 16

Production example (requires 16-24 GB GPU):
    python fine_tune.py \
        --model_name codellama/CodeLlama-7b-hf \
        --train_file data/train.jsonl \
        --val_file data/val.jsonl \
        --output_dir ./code-lora \
        --use_qlora
"""

import argparse
import json
import os
import sys
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


def parse_args():
    parser = argparse.ArgumentParser(description="LoRA/QLoRA fine-tuning for code generation")
    parser.add_argument("--model_name", default="codellama/CodeLlama-7b-hf", help="Base model to fine-tune")
    parser.add_argument("--train_file", default="data/train.jsonl", help="Training JSONL file")
    parser.add_argument("--val_file", default="data/val.jsonl", help="Validation JSONL file")
    parser.add_argument("--output_dir", default="./code-lora", help="Where to save the LoRA adapter")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--per_device_train_batch_size", type=int, default=4)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-4)
    parser.add_argument("--lora_r", type=int, default=16)
    parser.add_argument("--lora_alpha", type=int, default=32)
    parser.add_argument("--lora_dropout", type=float, default=0.05)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--use_qlora", action="store_true", help="Use 4-bit QLoRA")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def format_example(example: dict) -> str:
    instruction = example.get("instruction", "")
    output = example.get("output", "")
    return f"### Task: {instruction}\n### Response:\n{output}"


def main():
    args = parse_args()

    if not Path(args.train_file).exists():
        print(f"Training file not found: {args.train_file}", file=sys.stderr)
        sys.exit(1)

    if not Path(args.val_file).exists():
        print(f"Validation file not found: {args.val_file}", file=sys.stderr)
        sys.exit(1)

    torch.manual_seed(args.seed)

    # 1. Load model and tokenizer
    bnb_config = None
    if args.use_qlora:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        quantization_config=bnb_config,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token

    if args.use_qlora:
        model = prepare_model_for_kbit_training(model)

    # 2. Configure LoRA
    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # 3. Load and format data
    raw_datasets = load_dataset("json", data_files={"train": args.train_file, "validation": args.val_file})

    def tokenize_function(examples):
        size = len(next(iter(examples.values())))
        texts = [format_example({k: examples[k][i] for k in examples}) for i in range(size)]
        return tokenizer(
            texts,
            truncation=True,
            max_length=args.max_length,
            padding="max_length",
        )

    tokenized_datasets = raw_datasets.map(tokenize_function, batched=True, remove_columns=raw_datasets["train"].column_names)

    # 4. Train
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        fp16=not args.use_qlora,
        bf16=False,
        optim="adamw_torch",
        seed=args.seed,
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
    )

    trainer.train()
    model.save_pretrained(os.path.join(args.output_dir, "final"))
    tokenizer.save_pretrained(os.path.join(args.output_dir, "final"))
    print(f"Adapter saved to {args.output_dir}/final")


if __name__ == "__main__":
    main()
