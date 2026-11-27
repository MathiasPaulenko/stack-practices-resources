# Configurar índices de búsqueda de texto completo

Scripts ejecutables de búsqueda de texto completo en PostgreSQL: columnas `tsvector` generadas, índices GIN, ranking, resaltado, columnas ponderadas, consultas de frase/proximidad, coincidencia difusa con trigramas, vectores multi-idioma, actualización con triggers, configuraciones personalizadas y caché de búsqueda. Receta fuente: [Configurar índices de búsqueda de texto completo](https://stackpractices.com/es/recipes/sql-full-text-search-setup/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `setup-gin-index.sql` | Columna `tsvector` generada + índice GIN + búsqueda con ranking — el setup base |
| `headline-snippets.sql` | Snippets con `ts_headline` y ajuste de `MaxWords`/`MinWords` |
| `weighted-search.sql` | Ponderación `setweight` A/B para que el título gane al cuerpo |
| `phrase-proximity-search.sql` | `phraseto_tsquery`, operador `<->` y proximidad `<N>` |
| `trigram-fuzzy-search.sql` | Setup de `pg_trgm`, búsqueda por similitud, FTS+trigram combinado y autocomplete |
| `multi-language-search.sql` | Columna de idioma por fila alimentando `to_tsvector` |
| `index-maintenance.sql` | `fastupdate`, índices parciales, monitoreo de bloat y `ANALYZE` |
| `trigger-updates.sql` | Función trigger para mantener sincronizada una columna `search_vector` manual |
| `custom-text-search-config.sql` | Configuración + diccionario personalizado para terminología del dominio |
| `search-caching.sql` | Caché con vista materializada y búsqueda con facetas/agregación |

## Uso

Los ejemplos asumen una tabla `articles(id, title, body, category, status, language)`. Adapta los nombres de columna y la configuración de búsqueda (`'english'` vs `'spanish'`, etc.) a tu esquema — el stemming en el idioma equivocado es la razón más común de consultas que no devuelven nada.

Requiere PostgreSQL 12+ (columnas generadas). `pg_trgm` y `rum` son extensiones contrib: `CREATE EXTENSION pg_trgm;` necesita superusuario o el privilegio correspondiente en la nube.

## Punto clave

Indexa el `tsvector`, no el texto raw. Las columnas generadas se sincronizan solas; las manuales necesitan el trigger de `trigger-updates.sql`. Usa `pg_trgm` junto con FTS cuando necesites tolerancia a typos — `to_tsvector` solo no puede emparejar palabras parciales.
