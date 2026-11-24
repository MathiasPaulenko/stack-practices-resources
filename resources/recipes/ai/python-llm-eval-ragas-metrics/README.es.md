# Evalúa calidad RAG con métricas RAGAS

Proyecto ejecutable companion de la receta de StackPractices:
<https://stackpractices.com/es/recipes/python-llm-eval-ragas-metrics/>

## Archivos

- `eval_rag.py` — runner de evaluación completo: dataset de ejemplo con el esquema RAGAS 0.2+ (`user_input`/`response`/`retrieved_contexts`/`reference`), las cuatro métricas core, impresor de reportes formateado, `evaluate_rag_pipeline` para tu propio RAG y `evaluate_from_csv` para ejecuciones batch.

## Requisitos

```bash
pip install ragas langchain-openai datasets pandas
export OPENAI_API_KEY=...   # LLM evaluador + embeddings
```

## Ejecutar

```bash
python eval_rag.py
```

## Notas

- Los ejemplos apuntan a **RAGAS 0.2+**. Si tu código usa `question`/`answer`/`contexts`/`ground_truth`, renombra las columnas o fija `ragas<0.2`.
- Fija tu modelo evaluador por proyecto — los scores de distintos jueces no son comparables.
- El recall de contexto necesita respuestas `reference`; sin ellas solo obtienes tres de las cuatro métricas.
