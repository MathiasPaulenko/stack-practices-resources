# Fine-Tuning de LLM para Generación de Código — Companion

Esta carpeta contiene un companion en Python ejecutable para la receta de StackPractices [Fine-Tuning de un LLM para Generación de Código](https://stackpractices.com/es/recipes/llm-fine-tuning/).

Fine-tunea un modelo de lenguaje causal (por ejemplo, CodeLlama) con LoRA o QLoRA sobre un dataset en JSONL de tareas de código y respuestas.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `fine_tune.py` | Script principal de entrenamiento con argumentos CLI |
| `requirements.txt` | Dependencias de Python con versiones fijadas |
| `data/train.jsonl` | Ejemplos de entrenamiento (instruction + output) |
| `data/val.jsonl` | Ejemplos de validación |
| `README.md` | Versión en inglés |
| `README.es.md` | Este archivo |

## Inicio rápido

1. Instalá las dependencias:

```bash
pip install -r requirements.txt
```

1. Corré una prueba de humo con un modelo chico (CPU o una sola GPU):

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

1. Corré la receta de producción de 7B (requiere ~16-24 GB de VRAM con QLoRA):

```bash
python fine_tune.py \
    --model_name codellama/CodeLlama-7b-hf \
    --train_file data/train.jsonl \
    --val_file data/val.jsonl \
    --output_dir ./code-lora \
    --use_qlora \
    --num_train_epochs 3
```

## Formato del dataset

Cada línea de los archivos JSONL es un objeto con claves `instruction` y `output`:

```json
{"instruction": "Escribir una función Python que verifique si un número es primo", "output": "def es_primo(n):\n    ..."}
```

Reemplazá `data/train.jsonl` y `data/val.jsonl` con tu propio dataset curado antes de una corrida real de entrenamiento.

## Opciones del CLI

```text
--model_name                  Modelo base a fine-tunear (default: codellama/CodeLlama-7b-hf)
--train_file                  Archivo JSONL de entrenamiento (default: data/train.jsonl)
--val_file                    Archivo JSONL de validación (default: data/val.jsonl)
--output_dir                  Directorio donde guardar el adapter LoRA (default: ./code-lora)
--num_train_epochs            Cantidad de epochs (default: 3)
--per_device_train_batch_size Batch size por dispositivo (default: 4)
--gradient_accumulation_steps Pasos de acumulación de gradiente (default: 4)
--learning_rate               Learning rate (default: 2e-4)
--lora_r                      Rank r de LoRA (default: 16)
--lora_alpha                  Alpha de LoRA (default: 32)
--lora_dropout                Dropout de LoRA (default: 0.05)
--max_length                  Longitud máxima de secuencia (default: 512)
--use_qlora                   Habilitar QLoRA de 4 bits
--seed                        Semilla aleatoria (default: 42)
```

## Salida

El adapter LoRA entrenado se guarda en `OUTPUT_DIR/final/` junto con el tokenizador. Podés recargarlo con `peft.AutoPeftModelForCausalLM` o mergearlo en el modelo base para inferencia con vLLM.

## Links útiles

- [Paper de LoRA](https://arxiv.org/abs/2106.09685)
- [Paper de QLoRA](https://arxiv.org/abs/2305.14314)
- [Documentación de Hugging Face PEFT](https://huggingface.co/docs/peft)
- [Receta de StackPractices](https://stackpractices.com/es/recipes/llm-fine-tuning/)
