# Plantilla de Plan de Pruebas de Carga — Archivos complementarios

Archivos listos para usar que acompañan al documento de StackPractices:
<https://stackpractices.com/es/docs/load-test-plan-template/>

## Contenido

| Ruta | Qué muestra |
|------|-------------|
| `load-test-plan-template.md` | El documento de plan rellenable: objetivos, alcance, journeys, perfiles de carga, umbrales, monitoreo, reporting |
| `k6-load-test.js` | Script de k6 que implementa los tres journeys de ejemplo con stages, thresholds y métricas custom |
| `load-test-plan.jmx` | Plan de pruebas JMeter (JMX): 200 hilos, ramp-up de 300s, sampler de homepage con aserción de status 200 |
| `locustfile.py` | Archivo de Locust con tareas ponderadas (`@task`) que replican la distribución de tráfico de los journeys |
| `report-template.md` | Informe de prueba de carga de una página: configuración, resumen de resultados, cuellos de botella, recomendaciones |

## Ejecutar

```bash
# k6
k6 run k6-load-test.js

# Locust (sin UI, 200 usuarios, 34 min)
locust -f locustfile.py --headless -u 200 -r 30 -t 34m --host https://staging.example.com

# JMeter (modo GUI para editar, CLI para ejecutar)
jmeter -n -t load-test-plan.jmx -l results.jtl -e -o report/
```

Sustituye `staging.example.com` por tu entorno y ajusta la distribución de tráfico, los datos y los umbrales según las secciones §2–§4 del documento de plan.
