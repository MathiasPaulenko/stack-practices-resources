# Codificacion de URLs — Recursos Companion

Ejemplos ejecutables para la receta [Codificacion de URLs](https://stackpractices.com/es/recipes/url-encoding/).

## Archivos

| Archivo | Lenguaje | Descripción |
| --------- | -------- | ----------- |
| `url_encoding.py` | Python | Codificar, decodificar, construir query strings, parsear URLs con urllib |
| `url_encoding.js` | JavaScript | Codificar, decodificar, construir query strings, parsear URLs con URLSearchParams |
| `UrlEncoding.java` | Java | Codificar, decodificar, construir query strings, parsear URIs con URLEncoder |

## Inicio Rápido

### Python

```bash
python url_encoding.py
```

### JavaScript

```bash
node url_encoding.js
```

### Java

```bash
javac UrlEncoding.java && java UrlEncoding
```

## Puntos Clave

- Siempre codifica el input del usuario antes de colocarlo en una URL.
- Usa `encodeURIComponent` (JS), `quote` (Python) o `URLEncoder` (Java) para valores.
- Usa `%20` para paths y `+` para query strings legacy.
- Evita double-encoding: decodifica antes de recodificar si un valor puede ya estar codificado.
- Prefiere `URLSearchParams` (JS) y `urlencode` (Python) para construir queries.
