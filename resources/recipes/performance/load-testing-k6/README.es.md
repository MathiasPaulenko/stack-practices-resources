# Testing de carga de APIs con k6 — Recursos companion

Scripts k6 ejecutables para la receta [Testing de Carga de APIs con k6 y Aserciones de Umbral](https://stackpractices.com/es/recipes/load-testing-k6/).

## Contenido

| Archivo | Qué hace |
|---------|----------|
| `basic.js` | Rampa por etapas (100→200 VUs) con umbrales compuestos y `abortOnFail` |
| `scenario.js` | Escenario `ramping-arrival-rate` de modelo abierto apuntando a 100→300 RPS, umbrales por tag |
| `authenticated.js` | Login OAuth2 client-credentials en `setup()`, flujo carrito → checkout |
| `data.js` + `users.csv` | Datos de prueba desde CSV parseados con `SharedArray` y repartidos entre VUs |
| `smoke.js` | Gate de CI de 1 VU / 1 iteración con umbrales estrictos |
| `load-test-ci.yml` | GitHub Actions: smoke por PR, carga completa con `workflow_dispatch` |

## Uso

```bash
# instalar k6: https://k6.io/docs/get-started/installation/

# smoke test
k6 run --env BASE_URL=https://staging.example.com smoke.js

# prueba de carga por etapas
k6 run --env BASE_URL=https://staging.example.com basic.js

# escenario de tasa de llegada
k6 run --env BASE_URL=https://staging.example.com scenario.js

# flujo autenticado
k6 run --env BASE_URL=https://staging.example.com \
     --env CLIENT_ID=x --env CLIENT_SECRET=y authenticated.js

# logins desde CSV
k6 run --env BASE_URL=https://staging.example.com data.js

# métricas a Prometheus remote write
k6 run -o experimental-prometheus-rw basic.js
```

## Notas

- Apunta todo a staging — nunca a producción.
- Los umbrales incumplidos salen con código no-cero; eso es lo que convierte estos scripts en gates de CI.
- Vigila `dropped_iterations` en ejecuciones de tasa de llegada: significa que el generador no sostiene los RPS objetivo y los resultados adulan a la API.
