# Patrón Test Double: Reemplazar Dependencias con Stubs, Spies, Fakes

Implementaciones ejecutables de los cinco tipos de test doubles de Meszaros — dummy, stub, spy, fake, mock — en pytest y jest.

## Archivos

- `test_doubles.py` — ejemplos en pytest: dummy logger, stub de repository, spy con MagicMock, fake repository en memoria, mock con verificación de llamada exacta.
- `test_doubles.test.js` — equivalentes en jest: stubs/spies con `jest.fn()`, fake en memoria, verificación con mock.
- `package.json` — setup mínimo de jest.
- `pytest.ini` — config de descubrimiento de tests.

## Ejecutar

```bash
# Python
pip install pytest
pytest test_doubles.py

# JavaScript
npm install
npm test
```

Artículo fuente: https://stackpractices.com/es/patterns/test-double-pattern/
