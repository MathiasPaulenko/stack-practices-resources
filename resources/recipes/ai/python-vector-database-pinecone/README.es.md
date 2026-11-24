# Store vectorial Pinecone con embeddings de OpenAI

Complemento ejecutable de la receta de StackPractices
[Almacenar y consultar embeddings en Pinecone Vector Database](https://stackpractices.com/es/recipes/python-vector-database-pinecone/).

Implementación en un solo archivo que cubre:

- Creación de índice serverless (1536 dimensiones, métrica coseno)
- Embeddings con `text-embedding-3-small` de OpenAI + upsert con metadatos
- Búsqueda por similitud con filtros de metadatos (`$eq`, `$gte`, `$in`…)
- Namespaces para aislamiento multi-tenant
- Upserts por lotes con reintentos de backoff exponencial
- Búsqueda híbrida densa + sparse (`SparseValues`)
- Borrado por filtro, fetch por ID, `describe_index_stats()`

## Instalación

```bash
pip install -r requirements.txt
export PINECONE_API_KEY="tu-api-key-de-pinecone"
export OPENAI_API_KEY="tu-api-key-de-openai"
python pinecone_vector_store.py
```

`main()` ejecuta una demo mínima: upsert de tres documentos de ejemplo,
espera la propagación, imprime las estadísticas del índice y lanza una
consulta sin filtro y otra filtrada por metadatos.

## Notas

- El free tier cubre un índice serverless con 100K vectores.
- Los vectores recién insertados tardan unos segundos en ser consultables:
  usa `describe_index_stats()` en vez de verificar con una query inmediata.
- Cambiar a `text-embedding-3-large` requiere un índice nuevo de 3072 dimensiones.
