# Patrón Snapshot Testing — Recursos complementarios

Código de apoyo para el [Patrón Snapshot Testing](https://stackpractices.com/es/patterns/snapshot-testing-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `package.json` | JSON | Proyecto Jest mínimo (scripts `test`, `test:ci`, `test:update`) |
| `user_card.test.jsx` | JavaScript + Jest 29 | Snapshot externo, snapshot inline y property matchers para valores dinámicos |
| `test_snapshots.py` | Python 3.12+ | Ejemplos de pytest-snapshot y syrupy, incluido un snapshot de pedido normalizado |
| `normalize_response.py` | Python 3.12+ | Sustituye UUIDs y timestamps por placeholders estables antes del snapshot |
| `generate_nginx_config.py` | Python 3.12+ | Ejemplo de archivo generado: configuración de nginx determinista para capturar |
| `.github/workflows/test.yml` | YAML | Guarda en CI: `jest --ci` falla cuando falta una línea base o está desactualizada |
| `README.md` | Markdown | Versión en inglés de este archivo |

## Inicio rápido

### Jest

```bash
npm install
npm test            # la primera ejecución escribe las líneas base en __snapshots__/
npm test            # las siguientes comparan contra ellas
npm run test:update # regenera las líneas base tras un cambio intencional
npm run test:ci     # modo CI: falla en vez de escribir snapshots que faltan
```

### pytest

```bash
pip install pytest pytest-snapshot syrupy

pytest --snapshot-create   # pytest-snapshot: escribe las líneas base
pytest --snapshot-update   # syrupy / actualiza las líneas base
pytest                     # compara contra los snapshots guardados
```

### Configuración generada

```bash
python generate_nginx_config.py
# Imprime el bloque server de nginx determinista usado en el ejemplo de snapshot
```
