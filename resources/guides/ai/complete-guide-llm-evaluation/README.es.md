# Evaluación de LLM — Companion

Suite de evaluación ejecutable de [Guía Completa de Evaluación de LLM](https://stackpractices.com/es/guides/complete-guide-llm-evaluation/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `judge.py` | Judge por rúbrica + pairwise con posición aleatorizada + voto mayoritario |
| `ragas_eval.py` | Runner de RAGAS para datasets pregunta/respuesta/contexto/verdad |
| `regression_suite.py` | `LLMTestSuite` — casos de regresión en JSON con scoring Jaccard/judge |
| `ci_gate.py` | Gate bloqueante de CI con informe de fallos por test |
| `hallucination.py` | Chequeo de autoconsistencia + verificación afirmación-fuente |
| `ab_test.py` | Asignación A/B determinista + z-test + kappa de Cohen |
| `test_eval.py` | Tests unitarios offline — sin API key |
| `tests.json` | Dataset de regresión de ejemplo |
| `requirements.txt` | Dependencias fijadas |

## Inicio rápido

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
pytest test_eval.py -v   # corre completamente offline
python ragas_eval.py     # necesita API key
```
