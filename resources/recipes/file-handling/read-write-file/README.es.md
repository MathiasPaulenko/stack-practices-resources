# Leer y Escribir Archivos en Python, Node.js y Bash — Recursos complementarios

Archivos complementarios de [Leer y Escribir Archivos en Python, Node.js y Bash](https://stackpractices.com/es/recipes/read-write-file/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `safe_io.py` | `safe_write` (temporal + `os.replace` + `fsync`), `safe_read` con valor por defecto, `read_lines_lazy`, `write_json_atomic` |
| `stream-file.js` | Pipeline Transform línea a línea escribiendo a través de un archivo temporal, más helpers `readLines`/`appendLine` |
| `FileOps.java` | `atomicWrite` NIO (`ATOMIC_MOVE`), `safeRead`, `readLines`, `appendLine`, `processLines` |
| `safe-file-ops.sh` | `safe_write`, `safe_read`, `log_append`, `read_lines`, `create_secret_file` (`chmod 600`) en Bash |

## Cómo usarlo

1. `python safe_io.py` — escribe `demo.txt`, `state.json` e imprime lo releído.
2. `node stream-file.js` — procesa `input.log` → `output.log` en mayúsculas y añade una línea con timestamp a `app.log`.
3. `javac FileOps.java && java FileOps` — demo de escritura atómica + lectura segura + procesamiento por líneas.
4. `bash safe-file-ops.sh` — ejercita cada helper e imprime los resultados.

Sin dependencias — Python 3.10+, Node.js 18+, cualquier JDK moderno, Bash 4+.
