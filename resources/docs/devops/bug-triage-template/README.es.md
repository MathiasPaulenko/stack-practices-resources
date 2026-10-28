# Plantilla de Triaje de Bugs — Scripts Companion

Complemento de la plantilla de StackPractices [Plantilla de Triaje de Bugs](https://stackpractices.com/es/docs/bug-triage-template/).

| Archivo | Contiene |
|---|---|
| src/auto-triage.yml | Workflow de GitHub Actions que auto-etiqueta bugs por severidad |
| src/fingerprint.py | Normalización y fingerprinting de stack traces para deduplicar |
| src/sla-dashboard.py | Control de envejecimiento SLA con formato de alerta Slack |
| src/stale-bugs.sh | Consulta gh CLI para tickets S3/S4 obsoletos |
