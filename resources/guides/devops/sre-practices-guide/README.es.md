# Guía de Prácticas SRE — Kit complementario

Material complementario de [Ingeniería de confiabilidad del sitio (SRE)](https://stackpractices.com/es/guides/sre-practices-guide/).

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `alerting/burn-rate-alerts.yml` | Reglas de alertado Prometheus: burn rate multi-ventana para un SLO de 99.9% (niveles página + ticket) |
| `templates/slo-document.md` | Documento SLO para completar: definición de SLI, objetivo, alertado, política de presupuesto de error |
| `templates/postmortem-template.md` | Plantilla de postmortem sin culpa con línea de tiempo, factores contribuyentes y action items |

## Uso

1. Copiá `burn-rate-alerts.yml` a tu directorio de reglas de Prometheus y ajustá los multiplicadores (14.4x / 6x) y la base de ratio de error (0.001 para un SLO de 99.9%) a tu objetivo.
2. Completá `slo-document.md` por servicio y conseguí la firma de ingeniería y producto — una política de presupuesto que nadie firmó no frena lanzamientos.
3. Usá `postmortem-template.md` para cada incidente que toque el presupuesto de error; revisá los action items abiertos semanalmente.
