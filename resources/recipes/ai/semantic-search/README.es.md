# Búsqueda Semántica — Ejemplos Companion

Código companion para la [receta de búsqueda semántica](https://stackpractices.com/es/recipes/semantic-search/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `semantic_search_faiss.py` | Búsqueda semántica local con sentence-transformers + FAISS (gratis, sin API key) |
| `semantic_search_openai.py` | Búsqueda semántica con embeddings de OpenAI + FAISS (requiere `OPENAI_API_KEY`) |
| `semantic_search_js.js` | Búsqueda semántica en JavaScript con OpenAI + similitud coseno |
| `SemanticSearchService.java` | Servicio de producción en Java Spring AI + pgvector |
| `test_semantic_search.py` | Tests unitarios (se ejecutan sin dependencias externas) |

## Inicio rápido (FAISS local)

```bash
pip install sentence-transformers faiss-cpu numpy
python semantic_search_faiss.py
```

## Inicio rápido (OpenAI)

```bash
pip install openai faiss-cpu numpy
export OPENAI_API_KEY="tu-key"
python semantic_search_openai.py
```

## Ejecutar tests

```bash
pip install pytest numpy
pytest test_semantic_search.py -v
```

## Autor

Mathias Paulenko — [StackPractices.com](https://stackpractices.com)
