# Plantilla de Plan de Recuperación ante Desastres — Compañero

Recursos listos para copiar y escribir un plan de recuperación ante desastres:

- `dr-plan-template.md` — la plantilla DR completa: campos RTO/RPO, escenarios de riesgo, procedimientos de failover, runbook de recuperación, roles, calendario de tests y plan de comunicación.
- `failover-checklist.md` — checklist imprimible para correr un drill de failover, antes/durante/después.

## Uso

1. Copia `dr-plan-template.md` a tu repo o wiki y rellena los campos entre corchetes.
2. Define RTO/RPO por tier de servicio antes de escribir procedimientos — los números deciden la arquitectura, no al revés.
3. Usa `failover-checklist.md` en cada drill; un drill que no produce hallazgos no es un test real.

Artículo fuente: <https://stackpractices.com/es/docs/disaster-recovery-plan-template/>
