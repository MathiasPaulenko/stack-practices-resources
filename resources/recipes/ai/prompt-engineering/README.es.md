# Aplicar lo que funciona en Prompt Engineering — Ficheros complementarios

Recursos complementarios de la receta
[Aplicar lo que funciona en Prompt Engineering](https://stackpractices.com/es/recipes/prompt-engineering/).

## Contenido

| Fichero | Propósito |
|---------|-----------|
| `prompt-eval-suite.py` | Ejecuta un prompt contra un test set JSON y reporta pass/fail. Devuelve código de error bajo un umbral — usable como gate de CI para regresiones de prompts. |
| `few-shot-template.md` | Esqueleto reusable de prompt few-shot para tareas de clasificación/extracción. |
| `test-set.example.json` | Test set de ejemplo para clasificación de intención (10 pares input/expected). |

## Uso

```bash
pip install openai
export OPENAI_API_KEY=sk-...

python prompt-eval-suite.py \
  --test-set test-set.example.json \
  --system "Clasifica la intención del usuario en: SEARCH, SUPPORT, BILLING u OTHER." \
  --threshold 0.9
```

Tasa de aciertos por debajo del umbral → código de salida 1, fallos guardados en `eval-failures.json`.

## Licencia

Ver el fichero `LICENSE` en la raíz del repositorio.
