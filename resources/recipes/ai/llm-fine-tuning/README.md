# LLM Fine-Tuning for Code Generation — Companion

This folder contains a runnable Python companion for the StackPractices recipe [Fine-Tune a Language Model for Code Generation](https://stackpractices.com/recipes/llm-fine-tuning/).

It fine-tunes a causal language model (e.g., CodeLlama) with LoRA or QLoRA on a JSONL dataset of code tasks and responses.

## Files

| File | Purpose |
| --- | --- |
| `fine_tune.py` | Main training script with CLI arguments |
| `requirements.txt` | Python dependencies and pinned versions |
| `data/train.jsonl` | Example training examples (instruction + output) |
| `data/val.jsonl` | Example validation examples |
| `README.md` | This file |
| `README.es.md` | Spanish version |

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Run a smoke test on a small model (CPU or single GPU):

```bash
python fine_tune.py \
    --model_name Salesforce/codegen-350M-mono \
    --train_file data/train.jsonl \
    --val_file data/val.jsonl \
    --output_dir ./smoke-lora \
    --num_train_epochs 1 \
    --lora_r 8 \
    --lora_alpha 16
```

1. Run the production 7B recipe (requires ~16-24 GB VRAM with QLoRA):

```bash
python fine_tune.py \
    --model_name codellama/CodeLlama-7b-hf \
    --train_file data/train.jsonl \
    --val_file data/val.jsonl \
    --output_dir ./code-lora \
    --use_qlora \
    --num_train_epochs 3
```

## Dataset format

Each line in the JSONL files is an object with `instruction` and `output` keys:

```json
{"instruction": "Write a Python function that checks whether a number is prime", "output": "def is_prime(n):\n    ..."}
```

Replace `data/train.jsonl` and `data/val.jsonl` with your own curated dataset before a real training run.

## CLI options

```text
--model_name                  Base model to fine-tune (default: codellama/CodeLlama-7b-hf)
--train_file                  Training JSONL file (default: data/train.jsonl)
--val_file                    Validation JSONL file (default: data/val.jsonl)
--output_dir                  Where to save the LoRA adapter (default: ./code-lora)
--num_train_epochs            Number of training epochs (default: 3)
--per_device_train_batch_size Batch size per device (default: 4)
--gradient_accumulation_steps Gradient accumulation steps (default: 4)
--learning_rate               Learning rate (default: 2e-4)
--lora_r                      LoRA rank r (default: 16)
--lora_alpha                  LoRA alpha (default: 32)
--lora_dropout                LoRA dropout (default: 0.05)
--max_length                  Maximum sequence length (default: 512)
--use_qlora                   Enable 4-bit QLoRA
--seed                        Random seed (default: 42)
```

## Output

The trained LoRA adapter is saved to `OUTPUT_DIR/final/` along with the tokenizer. You can reload it with `peft.AutoPeftModelForCausalLM` or merge it into the base model for inference with vLLM.

## Useful links

- [LoRA paper](https://arxiv.org/abs/2106.09685)
- [QLoRA paper](https://arxiv.org/abs/2305.14314)
- [Hugging Face PEFT docs](https://huggingface.co/docs/peft)
- [StackPractices recipe](https://stackpractices.com/recipes/llm-fine-tuning/)
