# Runbook de Migración de Datos — Recursos Complementarios

Archivos complementarios de la [Plantilla de Runbook de Migración de Datos](https://stackpractices.com/es/docs/data-migration-runbook-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `migration-runbook.md` | Markdown | Runbook listo para adaptar: checklist pre-migración, tabla de estrategias, prueba en seco, ejecución, validación y rollback |
| `validate-migration.sh` | Bash | Comparación de conteos de filas entre bases de datos PostgreSQL fuente y destino, tabla por tabla |

## Inicio rápido

### 1. Copia el runbook

```bash
cp migration-runbook.md oncall/migrations/$(date +%Y-%m-%d)-mi-migracion.md
```

Rellena cada hueco `______`: hostnames, conteos de filas, umbrales, responsables y el registro de decisión.

### 2. Ejecuta el script de validación

```bash
export DB_NAME=mydb DB_USER=readonly
export TABLES="orders users payments"

./validate-migration.sh \
  --source source.db.internal \
  --target target.db.internal
```

El script imprime una comparación por tabla y sale con código distinto de cero si algún conteo no coincide — intégralo en los pasos de la prueba en seco y de la validación post-migración.

## Ensaya antes de producción

1. Ejecuta la sección de prueba en seco contra una copia de staging a escala de producción.
2. Registra las duraciones reales en el runbook — se convierten en la línea base de la próxima estimación.
3. Ensaya los pasos de rollback al menos una vez antes de la ventana de producción.

Consulta la [guía completa en StackPractices](https://stackpractices.com/es/docs/data-migration-runbook-template/) para la selección de estrategia, la resolución de problemas y los criterios de rollback.
