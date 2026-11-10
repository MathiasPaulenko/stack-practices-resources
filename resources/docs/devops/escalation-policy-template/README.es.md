# Recursos de la Plantilla de Política de Escalamiento

Recursos complementarios de [Plantilla de Política de Escalamiento](https://stackpractices.com/es/docs/escalation-policy-template/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `policy/escalation-policy-template.md` | Documento de política para completar: matriz de severidad, roster L1–L4, rutas de escalamiento temporizadas, canales de comunicación, reglas ante respondedores que no contestan y deberes de mantenimiento |
| `config/pagerduty-escalation-policy.yaml` | Políticas de escalamiento estilo PagerDuty para SEV 1 y SEV 2, con notas sobre la semántica de `escalation_delay_in_minutes` y `num_loops` |
| `config/opsgenie-escalation.json` | Payload de escalamiento estilo Opsgenie (reglas `if-not-acked` con delays temporizados y repetición) listo para adaptar a tus schedules |
| `templates/incident-communications.md` | Avisos listos para copiar en cada etapa: aviso inicial al cliente, actualización de progreso, resolución, ping interno de escalamiento y resumen ejecutivo |
| `templates/post-incident-review.md` | Plantilla de revisión post-incidente con sección dedicada a revisar el escalamiento que alimenta los cambios de la política |
| `checklists/escalation-drill.md` | Checklist de simulacro trimestral: recorre la escalera con una alerta sintética y verifica cada teléfono, delay y canal |

## Uso

1. Copia `policy/escalation-policy-template.md`, completa tu roster, SLAs y canales, y commitealo junto a tus runbooks.
2. Traduce la política a tu herramienta de alertas usando `config/` como referencia — recuerda que el delay de una regla es el timeout de ese nivel, no una espera antes de la primera alerta.
3. Fija `templates/incident-communications.md` en tu canal de incidentes para SEV 1–2.
4. Ejecuta `checklists/escalation-drill.md` cada trimestre; los datos de contacto caducan en silencio.
