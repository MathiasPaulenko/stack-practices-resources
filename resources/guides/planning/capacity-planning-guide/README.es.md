# Planificación de Capacidad — Prueba de Carga y Analizador de Cuellos de Botella

Código companion de la [guía de planificación de capacidad](https://stackpractices.com/es/guides/capacity-planning-guide/) de StackPractices.

## Archivos

- `src/capacity-test.js` — prueba de carga con k6 con rampa por etapas (100 → 200 VUs) y umbrales de p95 y tasa de error. Ejecuta con `k6 run capacity-test.js`; cambia el objetivo con `BASE_URL=https://tu.api`.
- `src/bottleneck_analyzer.py` — script en Python que evalúa el margen por recurso frente a umbrales de saturación e identifica cuál es tu techo de capacidad efectivo. Ejecuta con `python bottleneck_analyzer.py`.

## Requisitos

- Python 3.9+ (sin dependencias fuera de la librería estándar)
- [k6](https://k6.io/) para la prueba de carga
