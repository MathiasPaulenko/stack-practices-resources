# Plantilla de Prueba de Failover Cross-Region

Plantilla de ejecución para un simulacro de failover entre regiones que produce evidencias: roles, puertas go/no-go, criterios de aborto, línea de tiempo de failover/failback, informe post-prueba y un script Bash con guardas para Aurora Global Database + Route 53.

Artículo original: [Plantilla de Prueba de Failover Cross-Region](https://stackpractices.com/es/docs/cross-region-failover-template/)

## Archivos

- `failover-test-template.md` — plantilla en blanco lista para rellenar en cada simulacro
- `failover-test-example.md` — la misma plantilla completada para un simulacro de `payments-api`, incluyendo un informe con RTO no cumplido
- `failover.sh` — script de failover ejecutable con `--dry-run`, confirmación del operador, puerta de lag y verificación de convergencia DNS

## Cómo usarlo

1. Copia `failover-test-template.md` a tu runbook o herramienta de incidentes y rellena cada valor entre corchetes antes de abrir la ventana.
2. Ejecuta `failover.sh --dry-run` en el ensayo; imprime cada acción de AWS sin ejecutarla.
3. El día de la prueba, exporta las variables requeridas y corre `failover.sh`. Sale limpiamente si el health check de la secundaria o la puerta de lag de replicación fallan.
4. Mantén la secundaria en soak 30 minutos, ejecuta la sección de failback y adjunta el informe completado al registro de cambios.

Para un simulacro planificado sobre Aurora Global Database el script usa `switchover-global-cluster` (RPO 0). Para recuperación no planificada usa `failover-global-cluster`; para una réplica de lectura entre regiones independiente usa `promote-read-replica-db-cluster`. El artículo explica el script paso a paso.
