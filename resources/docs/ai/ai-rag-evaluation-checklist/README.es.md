# Checklist de Evaluación de RAG — Scripts de Apoyo

Scripts ejecutables para evaluar la calidad de un sistema RAG, que
acompañan al
[Checklist de Evaluación de RAG](https://stackpractices.com/es/docs/ai-rag-evaluation-checklist/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `eval_ragas.py` | Métricas RAGAS: fidelidad, relevancia de respuesta, precisión y recall de contexto |
| `eval_llm_judge.py` | Puntuación propia con LLM-as-judge (fidelidad, relevancia, corrección) para puertas de regresión |
| `requirements.txt` | Dependencias de Python |

## Requisitos

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=tu-clave
```

RAGAS usa un LLM internamente para varias métricas, así que se necesita
`OPENAI_API_KEY` (o un LLM alternativo configurado) para ambos scripts.

## Uso

```bash
python eval_ragas.py
python eval_llm_judge.py
```

Ambos scripts incluyen dos registros de ejemplo. Reemplaza `SAMPLES` /
`TEST_SET` con tuplas reales consulta-respuesta-contexto-referencia
capturadas de tu pipeline — 50+ elementos es el mínimo para una
puntuación con sentido.

Umbrales sugeridos antes del sign-off (ver el checklist):

- Precisión de contexto > 0.75 en k=5
- Recall de contexto > 0.80 en k=10
- Fidelidad > 0.90
- Corrección de respuesta > 0.85
