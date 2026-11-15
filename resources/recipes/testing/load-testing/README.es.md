# Pruebas de Carga en APIs con k6 y JMeter

Archivos ejecutables que acompañan a la [receta de pruebas de carga](https://stackpractices.com/es/recipes/load-testing/) en StackPractices.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `k6-load-test.js` | Script base de k6: rampa por etapas (100→200 VUs), umbrales de p95 y tasa de error |
| `k6-advanced.js` | Script avanzado de k6: reutilización de token con `setup()`, datos CSV con `SharedArray`, escenarios ponderados de navegación/carrito/checkout, umbral `abortOnFail` |
| `users.csv` | Archivo de credenciales de ejemplo que consume `k6-advanced.js` |
| `jmeter-test-plan.jmx` | Plan de pruebas JMeter completo: 100 hilos, rampa de 60s, 5 min de duración, aserción de respuesta |
| `load-test-ci.yml` | Pipeline de GitHub Actions: prueba de humo en PR + ejecución completa en ramas de release |
| `load-test-checklist.md` | Checklist previo para objetivo, generador, script y post-ejecución |

## Inicio rápido

```bash
# Ejecución base
k6 run k6-load-test.js

# Apuntando a un objetivo real
BASE_URL=https://staging.example.com k6 run k6-load-test.js

# Escenario avanzado (necesita CLIENT_SECRET para la petición del token OAuth)
BASE_URL=https://staging.example.com CLIENT_SECRET=xxx k6 run k6-advanced.js

# JMeter, sin interfaz
jmeter -n -t jmeter-test-plan.jmx -l results.jtl
```

Lee `load-test-checklist.md` antes de apuntar cualquiera de estos scripts a un entorno compartido.
