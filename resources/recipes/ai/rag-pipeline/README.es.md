# Pipeline RAG con LangChain y bases vectoriales

Companion ejecutable de [RAG con LangChain y bases vectoriales](https://stackpractices.com/es/recipes/rag-pipeline/).

## Qué incluye

- `rag_pipeline.py` — pipeline completo: cargar → fragmentar → embeber → almacenar en Chroma → recuperar → generar, con un prompt de fallback que responde "no lo sé" cuando falta contexto.
- `evaluate.py` — evaluación mínima de recuperación: ejecuta un pequeño conjunto de preguntas contra el almacén persistido e informa del hit rate.
- `knowledge_base.txt` — corpus de ejemplo (reembolsos, garantía, envíos, soporte, cuentas).
- `requirements.txt` — dependencias de LangChain/Chroma fijadas.

## Requisitos

- Python 3.10+
- Una API key de OpenAI (`OPENAI_API_KEY`) — usada para embeddings y generación con `gpt-4o-mini`.

## Ejecutar

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python rag_pipeline.py   # ingesta + dos preguntas respondidas + una pregunta de fallback
python evaluate.py       # comprobación del hit rate de recuperación
```

## Notas

- Usa los paquetes actuales de LangChain (`langchain-openai`, `langchain-chroma`, `langchain-community`). Los imports antiguos tipo `from langchain.embeddings import OpenAIEmbeddings` se eliminaron en versiones recientes.
- Para usar un modelo de embeddings local en lugar de OpenAI, cambia `OpenAIEmbeddings` por `HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")` de `langchain-huggingface` — no necesitas API key.
