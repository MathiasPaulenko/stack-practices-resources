# Pirámide de Tests — Recursos Companion

Código companion del [patrón Pirámide de Tests](https://stackpractices.com/es/patterns/test-pyramid-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `pricing.js` | JavaScript (ESM) | Lógica de dominio de precios que ejercitan los tests unitarios |
| `calculator.test.js` | JavaScript + Vitest | Ejemplo de capa unitaria: tests rápidos, aislados y deterministas |
| `pricing.py` | Python 3.10+ | La misma lógica de precios en Python |
| `test_pricing.py` | Python + pytest | Ejemplo de capa unitaria para la implementación Python |
| `checkout.e2e.spec.ts` | TypeScript + Playwright | Ejemplo de capa E2E: un journey crítico de checkout |
| `report_test_distribution.py` | Python 3.10+ | Cuenta tests por capa y avisa si los E2E superan el 15% |
| `smoke-test.sh` | Bash + curl + jq | Smoke check mínimo post-deploy |
| `test-pyramid-ci.yml` | GitHub Actions | Pipeline por capas: unitario → integración → E2E |

## Quick start

### Tests unitarios en JavaScript (Vitest)

```bash
npm install -D vitest
npx vitest run calculator.test.js
# Output: 5 passed
```

### Tests unitarios en Python (pytest)

```bash
python -m pytest test_pricing.py -v
# Output: 4 passed
```

### Medir la distribución de la pirámide de una suite

```bash
python report_test_distribution.py
# Unit:        312 (68%)
# Integration:  104 (23%)
# E2E:           41 (9%)
```

### Smoke test después de un deploy

```bash
BASE_URL=https://api.example.com ./smoke-test.sh
```

### Pipeline de CI por capas

Copiá `test-pyramid-ci.yml` a `.github/workflows/tests.yml`. Cada capa corre solo si la capa más barata de abajo pasó, manteniendo el feedback rápido y los minutos de CI bajos.
