# Gestión de deuda técnica — Companion ejecutable

Código de acompañamiento de la guía [Deuda Técnica: rastrear, priorizar, reducir](https://stackpractices.com/es/guides/complete-guide-technical-debt-management/).

## Archivos

- `debt-prioritizer.js` — puntúa ítems de deuda por impacto, interés y esfuerzo, y los ordena. Incluye el registro de ejemplo de la guía para ver por qué el ítem de tests de pagos supera a la refactorización de auth más grande.
- `measure-debt.js` — foto mensual de la deuda: conteo de TODO/FIXME y dependencias desactualizadas se calculan directamente; cobertura y duplicación se leen de `coverage/coverage-summary.json` y `report/jscpd-report.json` cuando ya ejecutas esas herramientas.
- `templates/debt-register.md` — el formato de registro con un ejemplo relleno.
- `templates/stakeholder-report.md` — el esqueleto del reporte top-cinco para pedir capacidad de repago a la dirección.

## Ejecutar

```bash
node debt-prioritizer.js
node measure-debt.js            # escanea el directorio actual
node measure-debt.js ../mi-app  # o apúntalo a un árbol de código
```

Salida esperada del priorizador: TD-002 primero (el impacto crítico gana al mayor esfuerzo), TD-003 último (bajo impacto, alto esfuerzo — el cuadrante de "ignorar").
