# Plantilla de Plan de Ejecución de Pruebas de Carga — Archivos complementarios

Archivos que acompañan a la [Plantilla de Plan de Ejecución de Pruebas de Carga](https://stackpractices.com/es/docs/load-test-execution-plan-template/) de StackPractices.

## Contenido

- `load-test-execution-plan-template.md` — la plantilla rellenable: objetivos y alcance, escenarios, criterios de éxito, preparación del entorno, línea temporal de ejecución T-menos, resultados y hallazgos con responsables.
- `execution-checklist.md` — un checklist imprimible del día de la prueba, desde T-1 día hasta los pasos posteriores.
- `k6-load-test.js` — un script de k6 ejecutable que escala hasta los usuarios virtuales del escenario pico, etiqueta las peticiones con un ID de correlación y frena la ejecución con una métrica de tasa de fallos personalizada.
- `locustfile.py` — la misma mezcla de escenarios como `HttpUser` de Locust con tareas ponderadas; se ejecuta con `locust -f locustfile.py --host <objetivo>`.

## Uso

1. Copia `load-test-execution-plan-template.md` en la documentación de tu equipo y rellena cada fila.
2. Recorre `execution-checklist.md` en orden durante la ventana de la prueba.
3. Adapta `k6-load-test.js` a tus endpoints y ejecútalo con `k6 run k6-load-test.js`.

La [Plantilla de Plan de Pruebas de Carga](https://stackpractices.com/es/docs/load-test-plan-template/) define los objetivos y umbrales que este plan ejecuta; la [Plantilla de Informe de Pruebas de Carga](https://stackpractices.com/es/docs/load-test-report-template/) es donde se archivan los hallazgos.
