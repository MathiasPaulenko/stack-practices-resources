# Patrón Embedding Cache — Implementaciones ejecutables

Compañero del patrón de StackPractices [Patrón Embedding Cache](https://stackpractices.com/es/patterns/embedding-cache-pattern/).

Un cache de embeddings con clave `modelo:SHA-256(texto)`, expiración por TTL, batch get-or-compute, estadísticas de hit rate e invalidación por modelo. Tres implementaciones equivalentes con función mock para correr sin API keys.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/embedding_cache.py` | Python 3.10+ (solo stdlib) | `python src/embedding_cache.py` |
| `src/embedding-cache.js` | Node.js 18+ (solo stdlib) | `node src/embedding-cache.js` |
| `src/EmbeddingCache.java` | Java 17+ | `javac src/EmbeddingCache.java && java -cp src EmbeddingCache` |

Cada ejecución procesa una lista corta de documentos con repetidos e imprime las estadísticas — verás cómo suben los hits y se detienen las llamadas API.
