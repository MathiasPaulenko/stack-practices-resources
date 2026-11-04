# LangChain en Producción — Companion

Proyecto Python ejecutable de la guía de StackPractices
[Guía Completa de LangChain en Producción](https://stackpractices.com/es/guides/complete-guide-langchain-production/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `chain.py` | Chain LCEL básico: prompt → modelo → parser |
| `parallel_chain.py` | Abanico con `RunnableParallel` (resumen + keywords + sentimiento) |
| `rag.py` | Pipeline RAG completo: carga → split → Chroma → retrieve → respuesta con citas |
| `agent.py` | Agente tool-calling con `max_iterations`/`max_execution_time` y matemáticas seguras con `asteval` |
| `app.py` | Endpoint FastAPI que streamea el chain por SSE |
| `test_chain.py` | Tests unitarios con `FakeListChatModel`, sin llamadas a la API |
| `requirements.txt` | Dependencias fijadas incluyendo paquetes partner |

## Inicio rápido

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# Ejecuta las piezas
python chain.py
python parallel_chain.py
python agent.py

# RAG necesita un documento que indexar
mkdir -p docs && echo "Vacation policy: 20 days per year." > docs/handbook.txt
python rag.py

# Sirve la API
uvicorn app:app --reload

# Los tests corren sin API key
pytest test_chain.py -v
```

`test_chain.py` y su test de fallback corren completamente offline. Todo lo
demás requiere `OPENAI_API_KEY`.
