# Escapar Entidades HTML — Recursos complementarios

Helpers ejecutables de escapado para los tres contextos de salida donde el escapado HTML por sí solo no basta —JSON embebido en `<script>` y atributos de URL— además del contexto clásico de cuerpo/atributo, en Python, JavaScript y Java.

Complemento de: https://stackpractices.com/es/recipes/escape-html-entities/

## Archivos

| Archivo | Lenguaje | Qué cubre |
|---------|----------|-----------|
| `escape_html.py` | Python | `html.escape`, serializador JSON para `<script>`, validador de URLs que rechaza `javascript:` |
| `test_escape_html.py` | Python | Suite pytest para los tres helpers |
| `escapeHtml.js` | JavaScript | Mapa manual de entidades, escapado por DOM, `safeJsonInScript`, `safeUrl` |
| `escapeHtml.test.js` | JavaScript | Suite con `node:test`, cero dependencias |
| `HtmlEscaper.java` | Java | Apache Commons Text + variantes por contexto del OWASP Encoder |

## Ejecutar los tests

```bash
# Python (solo stdlib, pytest para la suite)
python escape_html.py
pytest test_escape_html.py -v

# JavaScript (Node 18+, runner de tests integrado)
node --test escapeHtml.test.js
```

`HtmlEscaper.java` necesita `commons-text` y `owasp-encoder` en el classpath; es una implementación de referencia, no un proyecto compilable.

## Qué llevarte

- El escapado **depende del contexto**: cuerpo, atributo, `<script>`, URL y CSS necesitan codificaciones distintas.
- Las entidades HTML **no pueden proteger un bloque `<script>`** —escapa `<` como `\u003c` dentro del JSON embebido.
- Las URLs `javascript:` no contienen nada escapable; valida el **esquema**, no los caracteres.
- Escapa al renderizar y guarda la base de datos en crudo.
