# Sanitizar Input de Usuario — Recursos complementarios

Archivos companion de [Sanitizar Input de Usuario](https://stackpractices.com/es/recipes/sanitize-user-input/) en StackPractices.

## Archivos

| Archivo | Qué demuestra |
|---------|---------------|
| `path_traversal_guard.js` | Resolver un path de usuario bajo una base permitida y rechazar escapes `../` y null bytes |
| `nosql_sanitize.js` | Quitar operadores con prefijo `$` de objetos de query suministrados por el usuario |
| `validate_upload.py` | Detección de tipo por magic bytes y límites de tamaño (solo stdlib — el demo no necesita `magic`) |

## Cómo usar

```bash
node path_traversal_guard.js
node nosql_sanitize.js
python validate_upload.py
```

Sin dependencias más allá de Node.js ≥ 18 y Python ≥ 3.10.
