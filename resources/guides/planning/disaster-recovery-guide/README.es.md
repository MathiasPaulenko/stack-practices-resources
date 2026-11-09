# Recuperación ante Desastres — Recursos del Companion

Piezas ejecutables de la [guía de recuperación ante desastres](https://stackpractices.com/es/guides/disaster-recovery-guide/).

| Archivo | Qué es |
|---|---|
| `dr-tiers.yaml` | Mapeo de niveles de servicio a RTO/RPO/estrategia. Rellena tus propios servicios por nivel. |
| `postgres-backup.sh` | Backup de PostgreSQL: activa el archivado WAL, hace un `pg_basebackup` diario, lo envía a S3 en una segunda región y limpia los locales a los 7 días. |
| `test-backup-restore.py` | Verificación de restauración: restaura el backup más reciente en una base desechable y comprueba que una tabla crítica tiene filas. Prográmala — un backup que nunca restauras no es un backup. |
| `failover-runbook.md` | Runbook de failover de base de datos listo para copiar: disparador, pasos cronometrados y notas de rollback. |

## Inicio rápido

```bash
# 1. Edita dr-tiers.yaml con tus servicios.

# 2. Revisa postgres-backup.sh: configura BACKUP_DIR y S3_BUCKET.

# 3. Verifica que un backup se restaura de verdad (requiere pg_restore/psql + DB desechable):
export PGHOST=localhost PGUSER=postgres BACKUP_DIR=/backups CRITICAL_TABLE=orders
python test-backup-restore.py

# 4. Adapta failover-runbook.md a tu DNS, nombres de alerta y canales de comunicación.
```

Requisitos: herramientas de cliente de PostgreSQL (`pg_basebackup`, `pg_restore`, `psql`, `createdb`, `dropdb`), AWS CLI para la copia a S3 y Python 3.10+ para la verificación.
