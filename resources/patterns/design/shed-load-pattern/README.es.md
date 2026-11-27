# Patrón Shed Load — Ejemplos de código

Ejemplos complementarios del recurso [Patrón Shed Load](https://stackpractices.com/es/patterns/shed-load-pattern/) en StackPractices.

## Archivos

- `load_shedder.py` — Implementación en Python: descarte por umbrales sobre concurrencia, CPU (vía `psutil`), memoria y profundidad de cola, con estadísticas de aceptadas/descartadas.
- `load_shedder.js` — Implementación en Node.js: la misma lógica de admisión con `process.memoryUsage()` y handlers asíncronos.
- `LoadShedder.java` — Implementación en Java: contadores `AtomicInteger`, muestreo de memoria JVM y demo con `ExecutorService` en `main`.

## Ejecutar

```bash
# Python (requiere psutil)
pip install psutil
python load_shedder.py

# Node.js
node load_shedder.js

# Java
javac LoadShedder.java && java LoadShedder
```

Cada demo lanza 10 solicitudes concurrentes contra un shedder limitado a 3 concurrentes; espera ~3 aceptadas y ~7 descartadas con HTTP 503.

## Licencia

Los ejemplos de código se proporcionan con fines educativos como parte de StackPractices.
