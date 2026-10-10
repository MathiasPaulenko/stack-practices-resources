# Failover de Base de Datos — Recursos complementarios

Archivos complementarios del [Runbook de Failover de Base de Datos](https://stackpractices.com/es/docs/runbook-database-failover/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `failover-runbook.md` | Markdown | Runbook listo para adaptar: puertas de verificación, comandos de promoción para PostgreSQL/MySQL/RDS, checklist de cambio y acciones post-incidente |
| `failover.sh` | Bash | Script de failover automatizado con verificaciones pre-flight y puertas de seguridad `--dry-run` y `--force` |
| `patroni.yml` | YAML | Configuración de Patroni para failover automatizado de PostgreSQL con etcd como DCS |
| `verify-consistency.py` | Python | Verificación de consistencia post-failover: comparación de LSN, salud de slots de replicación y estimación de transacciones perdidas |

## Inicio rápido

### 1. Copia el runbook

```bash
cp failover-runbook.md oncall/failover-runbook.md
```

Rellena el nombre de tu servicio, hostnames (`*.db.internal`), roles de credenciales y umbrales de lag antes de que ocurra un incidente.

### 2. Prueba la automatización en seco

```bash
chmod +x failover.sh
./failover.sh --dry-run   # solo verificaciones pre-flight, sin cambios
./failover.sh             # ejecuta el failover real cuando haga falta
```

Edita `PRIMARY_HOST`, `REPLICA_HOST`, `DB_USER` y `MAX_LAG_SECONDS` al inicio del script para que coincidan con tu entorno.

### 3. Verifica después de la promoción

```bash
pip install psycopg2-binary
python verify-consistency.py
```

Configura `new_primary_host` y `old_primary_lsn` en la llamada de ejemplo al final del script.

## Puertas de decisión (valores del runbook)

| Puerta | Umbral | Acción |
|--------|--------|--------|
| Lag de réplica | < 5 segundos | Procede solo si se cumple; si no, espera o documenta la pérdida de datos |
| Lag post-promoción (nueva réplica) | < 1 segundo | Confirma antes de cerrar el incidente |
| Tasa de error tras el cambio | < 0.1% | Investiga antes de darlo por exitoso |

## Referencias

- [AWS RDS — Promover una réplica de lectura](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html#USER_ReadRepl.Promote)
- [Documentación de Patroni](https://patroni.readthedocs.io/en/latest/)
- [PostgreSQL — servidores standby con log shipping](https://www.postgresql.org/docs/current/warm-standby.html)
