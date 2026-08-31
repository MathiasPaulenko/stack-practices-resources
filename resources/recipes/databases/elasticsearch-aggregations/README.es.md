# Cómo usar agregaciones de Elasticsearch (con ejemplos)

Proyecto companion ejecutable para la receta de StackPractices.

## Qué contiene

- `python/products_aggregations.py` — inserta productos de ejemplo y ejecuta agregaciones `terms`, `stats` y `percentiles` con el cliente Python oficial.
- `javascript/search_client.mjs` — búsqueda facetada, histograma de ingresos y paginación compuesta con el cliente JavaScript oficial.
- `queries/` — consultas JSON copiar y pegar para la API REST de Elasticsearch.
- `docker-compose.yml` — un contenedor Elasticsearch 8.15.0 de un solo nodo.
- `requirements.txt` — dependencias de Python.
- `package.json` — dependencias de JavaScript.

## Ejecutar localmente con Docker

```bash
docker compose up -d
curl -f http://localhost:9200/_cluster/health
```

## Ejecutar el ejemplo de Python

```bash
python -m venv .venv
# en Windows: .venv\Scripts\activate
# en Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python python/products_aggregations.py
```

## Ejecutar el ejemplo de JavaScript

```bash
npm install
node javascript/search_client.mjs laptop
```

## Ejecutar las consultas JSON

```bash
# Crear el mapping del índice
curl -X PUT http://localhost:9200/products -H "Content-Type: application/json" -d @queries/setup_index.json

# Facetas por término
curl -X GET http://localhost:9200/products/_search -H "Content-Type: application/json" -d @queries/terms_facet.json
```

> Este es un entorno local de aprendizaje. Para producción, usá un clúster
> apropiado con seguridad habilitada y nodos maestro/datos dedicados.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `python/products_aggregations.py` | Ejemplos con el cliente Python y datos de muestra |
| `javascript/search_client.mjs` | Ejemplos con el cliente JavaScript |
| `queries/setup_index.json` | Mapping del índice con subcampos `keyword` |
| `queries/terms_facet.json` | Búsqueda facetada con `terms` |
| `queries/date_histogram_revenue.json` | Agregación de ingresos por serie temporal |
| `queries/composite_pagination.json` | Paginación profunda con `composite` |
| `docker-compose.yml` | Elasticsearch local de un nodo |
| `requirements.txt` | Dependencias de Python |
| `package.json` | Dependencias de JavaScript |

## Links

- Receta: <https://stackpractices.com/recipes/elasticsearch-aggregations/>
- Documentación de Elasticsearch: <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html>
