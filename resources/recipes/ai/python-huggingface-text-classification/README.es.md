# Fine-Tune y Despliega Clasificadores de Texto — Archivos complementarios

Ejemplos ejecutables de la receta
[Fine-Tune y Despliega Clasificadores de Texto con Hugging Face](https://stackpractices.com/es/recipes/python-huggingface-text-classification/).

## Archivos

- `train.py` — entrenamiento de punta a punta: carga un subset de 2k de IMDb, tokeniza con `AutoTokenizer`, hace fine-tuning de `distilbert-base-uncased` vía `Trainer` (F1 + accuracy) y guarda el mejor checkpoint junto al tokenizer en `./sentiment-classifier`.
- `infer.py` — `TextClassificationService` que envuelve `pipeline` para predicciones en batch con etiquetas legibles.
- `requirements.txt` — `transformers`, `datasets`, `evaluate`, `torch`, `accelerate`.

## Uso

```bash
pip install -r requirements.txt
python train.py   # ~5-10 min en una GPU T4, ~30-60 min en CPU
python infer.py
```

Se recomienda una GPU aunque no es obligatoria — el subset de IMDb es lo bastante pequeño para entrenar en CPU.
