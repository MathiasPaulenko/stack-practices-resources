# Plantilla de Control de Versiones de Prompts de IA

Recursos complementarios para la [Plantilla de Control de Versiones de Prompts de IA](https://stackpractices.com/es/docs/ai-prompt-version-control-template/) en StackPractices.com.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `prompt_metadata.yaml` | Archivo de metadatos de ejemplo con tres versiones, puntuaciones de evaluación y rutas de reversión |
| `eval_prompt.py` | Script de evaluación que ejecuta una versión del prompt contra un conjunto de prueba JSONL |
| `ab_test.py` | Harness de pruebas A/B que enruta tráfico entre dos versiones del prompt |
| `check_regression.py` | Verificación de regresión que compara resultados de evaluación antiguos vs nuevos |
| `prompt-eval.yml` | Workflow de GitHub Actions para evaluación automatizada de prompts en PR |

## Uso

1. Copia `prompt_metadata.yaml` en tu directorio de prompts.
2. Crea un subdirectorio `versions/` con un archivo `.md` por versión.
3. Crea un subdirectorio `eval/` con `test_set.jsonl` (200+ casos etiquetados).
4. Ejecuta `python eval_prompt.py --prompt prompts/classifier/prompt.md --test-set prompts/classifier/eval/test_set.jsonl --model gpt-4o-mini --threshold 0.88`.
5. Añade el workflow de GitHub Actions desde `prompt-eval.yml` a `.github/workflows/`.

## Numeración de Versiones

- **MAJOR**: Cambios disruptivos (cambio de modelo, cambio de esquema de salida, cambio de conjunto de categorías). Requiere re-evaluación y aprobación de stakeholders.
- **MINOR**: Adiciones de funcionalidades (nueva categoría, nuevo ejemplo few-shot, system prompt reestructurado). Requiere evaluación pero no aprobación de stakeholders.
- **PATCH**: Optimizaciones (reducción de tokens, ajustes de redacción, cambios de formato). Requiere evaluación, aprobación rápida.
