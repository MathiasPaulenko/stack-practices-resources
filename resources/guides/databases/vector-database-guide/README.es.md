# Base de Datos Vectorial — Pipeline RAG con pgvector

Pipeline RAG ejecutable con pgvector: contenedor Postgres + pgvector, esquema con índice HNSW ajustado, ingestión por chunks con embeddings de OpenAI, y un script de consulta que responde con citas de fuentes.

Código de acompañamiento de la guía de StackPractices:
[Bases de Datos Vectoriales: Embeddings y Búsqueda Semántica](https://stackpractices.com/es/guides/vector-database-guide/)

## Instalación

```bash
docker compose up -d          # Postgres 16 + pgvector, esquema auto-aplicado
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Uso

```bash
mkdir docs && cp /ruta/a/*.md docs/     # agrega tus documentos
python ingest.py docs/                  # fragmenta, embebe, almacena
python query.py "¿Cómo funcionan los índices vectoriales?"
```

## Archivos

| Archivo | Contenido |
|---|---|
| `docker-compose.yml` | Contenedor pgvector/pgvector:pg16 |
| `schema.sql` | Tabla `doc_chunks` + índice HNSW (m=16, ef_construction=64) |
| `ingest.py` | Fragmentación (~500 tokens, 10% overlap) + embedding + insert |
| `query.py` | `rag_query`: búsqueda por similitud + respuesta GPT-4o con citas |
| `requirements.txt` | openai, psycopg2-binary, pgvector |

## Notas

- `register_vector(conn)` del paquete `pgvector` es necesario para que psycopg2 serialice `list[float]` al tipo vector.
- Los embeddings son específicos del modelo: si cambias `text-embedding-3-small` por otro modelo, re-embebe todo — los vectores no son comparables entre modelos.
- Ajusta `ef_search` en consulta (`SET hnsw.ef_search = 40`) para negociar recall por latencia.
