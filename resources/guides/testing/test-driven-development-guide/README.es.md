# Desarrollo Guiado por Pruebas — Companion

Companion ejecutable de la [guía de Desarrollo Guiado por Pruebas](https://stackpractices.com/es/guides/test-driven-development-guide/) en StackPractices. Dos artefactos de la guía hechos ejecutables:

| Directorio | Qué es |
|-----------|--------|
| `python/` | El `ShoppingCart` construido ciclo a ciclo en la guía, más la suite pytest completa — cada test corresponde a un ciclo red-green-refactor. |
| `node/` | La suite Jest + supertest de `POST /api/transfers` de "TDD en Producción". El `describe` viene con `.skip`: conecta tu app Express, `getAccount` y el token de auth en los stubs marcados y quita el skip. |

## Ejecutarlo

```bash
# Python (5 tests)
cd python && pip install -r requirements.txt && pytest -x -q

# Node.js — tras conectar tu app en transfers.test.js
cd node && npm install && npm test
```

## Qué demuestra cada archivo

- `python/test_shopping_cart.py` — un test por ciclo TDD: carrito vacío (red), agregar items, descuento, caso límite (código inválido), ejemplo de naming con comentarios Arrange/Act/Assert.
- `node/transfers.test.js` — nombres de test a nivel de comportamiento (`debe rechazar...`), un bloque de afirmaciones por comportamiento, expectativas deterministas.

Guía original: https://stackpractices.com/es/guides/test-driven-development-guide/
