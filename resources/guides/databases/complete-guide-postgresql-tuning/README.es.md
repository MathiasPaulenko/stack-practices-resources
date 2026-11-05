# Configuraciones de Optimización de PostgreSQL

Recursos complementarios de la [Guía Completa de Optimización de PostgreSQL](https://stackpractices.com/es/guides/complete-guide-postgresql-tuning/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `postgresql-4gb.conf` | Perfil de ajuste para host dedicado de 4GB |
| `postgresql-16gb.conf` | Perfil de ajuste para host dedicado de 16GB |
| `postgresql-64gb.conf` | Perfil de ajuste para host dedicado de 64GB |
| `pgbouncer.ini` | Configuración de pool PgBouncer (modo transaction, auth SCRAM) |
| `pgbench-baseline.sh` | Script de benchmark de base — ejecútalo antes y después de ajustar |
| `monitoring-queries.sql` | Todas las consultas de monitorización de la guía, listas para ejecutar |

## Uso

1. Elige el perfil más cercano a la RAM de tu host e intégralo en `postgre
