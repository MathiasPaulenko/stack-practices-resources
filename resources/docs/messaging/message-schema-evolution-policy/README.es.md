# Política de Evolución de Esquemas de Mensajes — Recursos complementarios

Archivos de apoyo para la [Política de Evolución de Esquemas de Mensajes](https://stackpractices.com/es/docs/message-schema-evolution-policy/) en StackPractices.

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `order-created-v1.avsc` | Esquema Avro original (v1) usado en los ejemplos del documento. |
| `order-created-v2.avsc` | v2 compatible hacia atrás: `currency` opcional, `legacyPaymentMethod` deprecated, array de reemplazo `paymentMethods`. |
| `order-created.proto` | Protobuf v2 con número de campo reservado, campo deprecated y reemplazo repeated — las reglas de la política aplicadas. |
| `schema-compatibility-check.sh` | Script de CI: envía un esquema candidato al endpoint de compatibilidad del registry y falla el build con `is_compatible: false`. |
| `consumer-migration-checklist.md` | Checklist por consumidor para el procedimiento de cambio rupturista (escritura dual → migración → periodo de gracia → eliminación). |

## Uso

Integra `schema-compatibility-check.sh` en tu pipeline para que cada PR que toque un archivo de esquema se valide antes del merge:

```bash
./schema-compatibility-check.sh order-created-v2.avsc prod.orders.order-created.v1-value http://schema-registry:8081
```

## Fuente

- Documento: https://stackpractices.com/docs/message-schema-evolution-policy/
- Documento (ES): https://stackpractices.com/es/docs/message-schema-evolution-policy/
