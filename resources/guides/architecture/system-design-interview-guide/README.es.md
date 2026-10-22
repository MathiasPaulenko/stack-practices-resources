# Entrevistas de System Design — Artefactos

Archivos de apoyo para [Entrevistas de System Design: Framework, Ejemplos y Práctica](https://stackpractices.com/es/guides/system-design-interview-guide/).

Estos artefactos acompañan el ejemplo resuelto del acortador de URLs para que
puedas ensayar la matemática de capacidad e inspeccionar los esquemas en lugar
de solo leerlos.

## Archivos

- `capacity_estimator.py` — imprime escrituras/s, lecturas/s, ratio L/E y
  proyecciones de almacenamiento a partir de volúmenes diarios. Ejecútalo,
  luego cambia las entradas y explica en voz alta cómo cambiaría la arquitectura.
- `schema.sql` — tabla PostgreSQL para el mapeo de URLs (camino de escritura, OLTP).
- `click_events.cql` — tabla Cassandra para la analítica append-only de clics.
- `api.http` — el contrato de API de tres endpoints (acortar, redirigir, stats)
  en formato REST Client.

## Uso

```bash
python capacity_estimator.py
# Writes : 100,000,000/day  ≈ 1,157/s (peak ~3,472/s)
# Reads  : 10,000,000,000/day  ≈ 115,741/s (peak ~347,222/s)
# R/W ratio: 100:1
# Storage: 60 GB/day ≈ 22 TB/year (~110 TB over 5 years)
```

Usa tus propios números al practicar otros problemas: el hábito de cuantificar
antes de dibujar cajas es la habilidad que se está ensayando.
