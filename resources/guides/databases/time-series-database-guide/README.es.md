# Guía de Bases de Datos de Series Temporales — Companion

Archivos complementarios de la [Guía de Bases de Datos de Series Temporales](https://stackpractices.com/es/guides/time-series-database-guide/) en StackPractices.com.

## Archivos

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| `timescaledb-setup.sql` | SQL | Setup mínimo de TimescaleDB: extensión, hypertable, agregado continuo, políticas de retención y refresco |
| `iot-timescaledb-scenario.sql` | SQL | El escenario IoT completo de la guía: 10K sensores, agregados continuos por niveles, retención por niveles, consultas típicas |
| `engine-comparison.md` | Markdown | Notas de decisión InfluxDB vs TimescaleDB vs ClickHouse, referencia de line protocol y guía del `ORDER BY` de ClickHouse |

## Uso

1. Levanta PostgreSQL con la extensión TimescaleDB (la imagen Docker `timescale/timescaledb` funciona directamente).
2. Ejecuta `timescaledb-setup.sql` para el ejemplo mínimo funcional.
3. Ejecuta `iot-timescaledb-scenario.sql` para reproducir el escenario IoT de la guía de principio a fin.

## Notas

- Los fragmentos de InfluxDB y ClickHouse están inline en `engine-comparison.md` — ilustran sintaxis, no un setup ejecutable.
- Vigila la cardinalidad de las series antes de escalar la ingesta: los valores de tag sin límite son la forma más común de tumbar una TSDB.
