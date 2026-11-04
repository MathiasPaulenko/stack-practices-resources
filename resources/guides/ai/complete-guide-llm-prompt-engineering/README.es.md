# Guía Completa de Prompt Engineering para LLMs - Ejemplos de Código

Ejemplos ejecutables de la guía:
<https://stackpractices.com/es/guides/complete-guide-llm-prompt-engineering/>

## Instalación

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `prompts.py` | Contratos de system prompt + delimitadores de contenido no confiable |
| `few_shot.py` | Clasificación zero-shot vs few-shot |
| `self_consistency.py` | Muestreo CoT con voto mayoritario (n=5) |
| `structured_output.py` | Modo JSON + validación con Pydantic + reintento de reparación |
| `rag_grounding.py` | Índice de embeddings único + respuesta fundamentada |
| `function_calling.py` | Bucle de tools en dos pasos con llamadas en paralelo |
| `eval_harness.py` | Gate de regresión con dataset dorado para cambios de prompt |
| `tests.json` | Dataset dorado usado por el harness |

## Verificación sin conexión

```bash
python eval_harness.py --dry-run
```

Valida el dataset y el cableado sin llamadas a la API. Las ejecuciones
reales necesitan `OPENAI_API_KEY` y unos céntimos de `gpt-4o-mini`.
