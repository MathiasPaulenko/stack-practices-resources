# Patrón Specification — Companion

Specifications de facturas componibles con sobrecarga de operadores (`&`, `|`, `~`)
y un repository que acepta cualquier spec. Incluye cobertura pytest para specs
hoja y cada operador de composición.

## Ejecutar

```bash
pip install -r requirements.txt
python specifications.py   # imprime las facturas críticas
pytest                     # corre los tests de composición
```

## Qué mirar

- `specifications.py` — ABC `Specification`, compuestas `_And`/`_Or`/`_Not`, specs concretas, `InvoiceRepository`
- `tests/test_specifications.py` — tests de límite más un test por operador

Patrón original: <https://stackpractices.com/es/patterns/specification-pattern/>
