# Evolución de Schema de Base de Datos — Recursos complementarios

Archivos ejecutables de la receta [Evolución de Schema de Base de Datos](https://stackpractices.com/es/recipes/schema-evolution/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `expand_contract_postgres.sql` | El renombrado expand-contract en tres fases (`ADD` → dual-write → `DROP`) en PostgreSQL con backfill por lotes. |
| `pt_online_schema_change.sh` | Invocación de `pt-online-schema-change` de Percona para agregar un índice en una tabla MySQL grande sin bloquearla. Las credenciales vienen de variables de entorno. |
| `gh_ost_online_change.sh` | Invocación de `gh-ost` de GitHub para la misma clase de cambio; sincronización por binlog, sin triggers. Falla rápido si falta `MYSQL_PASSWORD`. |
| `liquibase_changelog.xml` | Changelog de Liquibase con la secuencia expand-contract expresada en tres changeSets (agregar columna → backfill → eliminar columna vieja). |
| `V1_2__add_user_preferences.sql` | Migración versionada estilo Flyway que crea la tabla `user_preferences`. |
| `not_null_and_fk_safely.sql` | Cómo agregar constraints `NOT NULL`, `CHECK` y `FOREIGN KEY` en tablas PostgreSQL vivas con el patrón `NOT VALID` + `VALIDATE`. |
| `split_column_trigger.sql` | División de `full_name` en `first_name`/`last_name` con un trigger plpgsql de dual-write que mantiene ambas representaciones sincronizadas. |
| `migration_session_settings.sql` | Guardas de sesión (`lock_timeout`, `statement_timeout`), chequeo de lag de replicación y `ANALYZE` tras los backfills. |

## Uso

- **PostgreSQL**: ejecuta los `.sql` primero en una copia de staging — `psql -f expand_contract_postgres.sql`. Corre `migration_session_settings.sql` al inicio de cada sesión de migración.
- **MySQL**: `bash gh_ost_online_change.sh` o `bash pt_online_schema_change.sh` con `MYSQL_HOST`/`MYSQL_USER`/`MYSQL_PASSWORD`/`MYSQL_DB` exportadas.
- **Flyway/Liquibase**: coloca los archivos SQL/XML en tu directorio de migraciones y deja que la herramienta los aplique en orden.

Todos los scripts asumen reejecución: usa `IF (NOT) EXISTS` donde tu versión lo soporte y prueba siempre el rollback en staging antes de producción.
