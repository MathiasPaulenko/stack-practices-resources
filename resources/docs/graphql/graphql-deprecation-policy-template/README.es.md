# Plantilla de Política de Deprecación de GraphQL — Código complementario

Recursos complementarios para [Plantilla de Política de Deprecación de GraphQL](https://stackpractices.com/es/docs/graphql-deprecation-policy-template/)
(EN: [GraphQL Deprecation Policy Template](https://stackpractices.com/docs/graphql-deprecation-policy-template/)).

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `tracking/apollo-server-4-deprecation-plugin.ts` | Plugin de Apollo Server 4 que recorre cada query con `TypeInfo`/`visitWithTypeInfo`, reporta el uso de campos deprecados a analítica e inyecta `extensions.deprecations` en la respuesta |
| `communication/deprecation-email-template.md` | Email de aviso de deprecación listo para copiar, con conteo de uso, impacto, enlace a la guía de migración y el cronograma anuncio → aviso → aviso final → eliminación |
| `reports/usage-report-template.txt` | Informe semanal de uso de campos deprecados: conteos por campo, principales clientes, tendencia y elegibilidad de eliminación |
| `templates/migration-guide-template.md` | Esqueleto de guía de migración: qué cambió, queries antes/después, pasos de migración, problemas comunes y cronograma |

## Uso

1. Registra `deprecationTracker` como plugin de Apollo Server 4 y conecta `analytics.track` a tu pipeline (Segment, logs, etc.).
2. Despliégalo y recoge una línea base antes de anunciar cualquier deprecación — el primer email debería incluir cifras reales por cliente.
3. Envía `deprecation-email-template.md` a los consumidores los días 0, 30, 90 y 180; rellena los `{placeholders}` desde el informe de uso.
4. Publica una `migration-guide-template.md` por cada elemento deprecado y enlázala desde el `reason` de `@deprecated`.
5. Elimina un elemento solo tras 30 días consecutivos de uso cero, siguiendo el checklist de la página principal.

## Licencia

MIT — ver la raíz del repositorio.
