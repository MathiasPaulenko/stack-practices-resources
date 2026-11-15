# Convención de Nombres de Tópicos de Kafka — Archivos Companion

Archivos que acompañan a la plantilla de StackPractices: un script de lint que valida nombres de tópicos contra `<entorno>.<dominio>.<entidad>.<tipo>[.<versión>]`, un ticket de solicitud listo para rellenar y ejemplos de `kafka_topic` en Terraform.

Companion de: https://stackpractices.com/es/docs/kafka-topic-naming-convention-template/

## Archivos

- `naming-lint.sh` — valida nombres de tópicos por stdin, sale con código distinto de cero si hay violaciones
- `topics.txt` — lista de ejemplo (mezcla de nombres válidos e inválidos)
- `kafka-topics.tf` — ejemplos Terraform para tópicos event, snapshot (compactados) y DLQ
- `topic-request-template.md` — plantilla de ticket para el flujo de creación

## Ejecutar el linter

```bash
./naming-lint.sh < topics.txt
```

Salida esperada: los seis primeros nombres pasan, los cinco últimos fallan con el motivo.
