# Analizar Archivos Markdown — Archivos complementarios

Archivos complementarios de [Analizar Archivos Markdown](https://stackpractices.com/es/recipes/parse-markdown-files/) en StackPractices.

## Contenido

- `parse_markdown.py` — `to_html` con extensiones explícitas, `split_frontmatter`, `extract_headings` y `extract_links`.
- `post.md` — post de ejemplo con frontmatter YAML, encabezados, una tabla y un link.
- `test_parse_markdown.py` — suite pytest. Ejecuta: `pytest test_parse_markdown.py -v` (requiere `pip install markdown`).

## Qué mirar

- `split_frontmatter` primero, luego parsear — pasar `---` al parser produce un encabezado espurio.
- `test_to_html_table_needs_extension` muestra que las tablas son una extensión opt-in, no Markdown núcleo.
