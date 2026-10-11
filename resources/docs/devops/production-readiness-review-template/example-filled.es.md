# PRR: Servicio de Notificaciones en Tiempo Real

## Servicio

- Nombre: notification-service
- Tipo: Microservicio (Go)
- Tier: 1 (Crítico para experiencia de usuario)
- Fecha de revisión: 2026-07-11

## Hallazgos de Revisión

| Item | Hallazgo | Riesgo | Mitigación | Responsable | Fecha |
|------|----------|--------|------------|-------------|-------|
| Observabilidad | No hay dashboard de WebSocket | Medio | Crear dashboard antes de lanzar | alice | 2026-07-15 |
| Alertas | No hay alerta para conexiones rechazadas | Alto | Agregar alerta antes de lanzar | bob | 2026-07-14 |
| Seguridad | Validación JWT sin test de expiración | Alto | Agregar test antes de lanzar | carol | 2026-07-14 |
| Documentación | No existe runbook de rollback | Medio | Escribir runbook antes de lanzar | alice | 2026-07-16 |
| Operacional | On-call no entrenado en WebSocket | Medio | Sesión de capacitación | platform | 2026-07-18 |

## Sign-Off

| Rol | Nombre | Fecha | Decisión |
|-----|--------|-------|----------|
| Dueño de ingeniería | alice | 2026-07-18 | Aprobar condicional |
| Product owner | dave | 2026-07-18 | Aprobar |
| Revisor de seguridad | carol | 2026-07-18 | Aprobar (test agregado) |
| SRE / Plataforma | bob | 2026-07-18 | Aprobar condicional |

## Decisión

Aprobado condicionalmente. Lanzamiento permitido después de
completar los 3 items de riesgo Alto (alertas, seguridad, test).
Items de riesgo Medio rastreados con fechas límite pero no
bloquean el lanzamiento.
