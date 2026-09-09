# Copiar y Mover Archivos — Ejemplos Companion

Código companion para la [receta de copiar y mover archivos](https://stackpractices.com/es/recipes/copy-move-files/).

## Archivos

| Archivo | Descripción |
| ------- | ------------ |
| `safe_copy.py` | Python: copiar/mover seguro con shutil, pathlib y verificación SHA-256 |
| `copy_move.js` | JavaScript: copiar/mover con fs.promises, checksums y fallback EXDEV |
| `FileCopier.java` | Java NIO: copiar/mover con ATOMIC_MOVE y fallback entre dispositivos |
| `safe_copy.sh` | Bash: copia segura con sha256sum y copia por lotes |
| `test_copy_move.py` | Tests unitarios (se ejecutan sin dependencias externas) |

## Inicio rápido (Python)

```bash
python safe_copy.py
```

## Inicio rápido (JavaScript)

```bash
node copy_move.js
```

## Ejecutar tests

```bash
pip install pytest
pytest test_copy_move.py -v
```

## Autor

Mathias Paulenko — [StackPractices.com](https://stackpractices.com)
