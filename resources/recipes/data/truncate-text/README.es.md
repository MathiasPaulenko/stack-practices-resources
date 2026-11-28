# Truncar Texto

Ejemplos ejecutables de [stackpractices.com/es/recipes/truncate-text/](https://stackpractices.com/es/recipes/truncate-text/).

| Archivo | Muestra |
|---------|---------|
| `truncate_text.py` | Slice por carácter + `textwrap.shorten` por palabra |
| `truncate-text.js` | Slice por carácter, límite de palabra y corte seguro con `Intl.Segmenter` |
| `TextTruncator.java` | `StringUtils.abbreviate` + bucle por palabra |
| `truncate.css` | `text-overflow: ellipsis` de una línea y `line-clamp` multilínea |

## Ejecutar

```bash
python truncate_text.py
node truncate-text.js
javac TextTruncator.java && java TextTruncator
```

Para texto de UI, prefiere CSS: el string completo sigue en el DOM y nada se destruye.
