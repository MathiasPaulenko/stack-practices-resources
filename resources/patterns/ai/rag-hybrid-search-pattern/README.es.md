# Patrón de búsqueda híbrida para RAG — Ejemplos ejecutables

Companion del patrón de StackPractices [Búsqueda híbrida para RAG](https://stackpractices.com/es/patterns/rag-hybrid-search-pattern/).

Los tres programas ejecutan una búsqueda por palabras clave, otra por similitud coseno y Reciprocal Rank Fusion sobre un corpus pequeño en memoria. Los vectores son valores de muestra fijos, no embeddings generados por un modelo. No hace falta una base de datos, conexión de red ni clave de API.

## Ejecución

| Archivo | Requisito | Comando |
| --- | --- | --- |
| `src/hybrid_search.py` | Python 3.10+ | `python src/hybrid_search.py` |
| `src/hybrid-search.js` | Node.js 18+ | `node src/hybrid-search.js` |
| `src/HybridSearch.java` | Java 17+ | `javac src/HybridSearch.java && java -cp src HybridSearch` |

En un sistema RAG real, sustituye las funciones de BM25 y búsqueda vectorial de muestra por los recuperadores de tu motor. Mantén las listas ordenadas por relevancia y pásalas a `reciprocalRankFusion`.
