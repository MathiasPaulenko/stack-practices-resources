# Recursos de recuperación ante desastres

Piezas ejecutables de la [guía de recuperación ante desastres](https://stackpractices.com/es/guides/disaster-recovery-guide/).

| Archivo | Qué incluye |
|---|---|
| `dr-tiers.yaml` | Mapeo de niveles de servicio a objetivos RTO/RPO y estrategia. Completa los servicios por nivel. |
| `postgres-backup.sh` | Crea un backup físico diario con `pg_basebackup` y archivos lógicos `pg_dump` en formato personalizado para las bases elegidas; los envía a S3. |
| `test-backup-restore.py` | Restaura el archivo lógico `.dump` más reciente en una base desechable y comprueba una tabla configurada. No restaura el tar del backup físico. |
| `failover-runbook.md` | Runbook de failover de base de datos: disparador, pasos cronometrados y notas de rollback. |

## Inicio rápido

```bash
# 1. Edita dr-tiers.yaml con tus servicios.

# 2. Configura BACKUP_DIR, S3_BUCKET y DATABASES en postgres-backup.sh.
# DATABASES es una lista separada por comas, por ejemplo: app,reporting.

# 3. Ejecuta el script con PostgreSQL y AWS ya configurados.
./postgres-backup.sh

# 4. Restaura el archivo lógico en una base desechable y comprueba una tabla real.
export PGHOST=localhost PGUSER=postgres BACKUP_DIR=/backups CRITICAL_TABLE=public.orders
python test-backup-restore.py

# 5. Adapta failover-runbook.md a tu DNS, alertas y canales de comunicación.
```

El backup físico y los archivos lógicos son artefactos distintos. La prueba usa un `.dump` creado con `pg_dump --format=custom`; no demuestra que la recuperación física ni la reproducción de WAL funcionen. Haz un simulacro físico separado.

Requisitos: herramientas cliente de PostgreSQL (`pg_basebackup`, `pg_dump`, `pg_restore`, `psql`, `createdb`, `dropdb`), AWS CLI, Bash y Python 3.10+. La base destino debe ser desechable: el script la elimina antes de restaurar.
