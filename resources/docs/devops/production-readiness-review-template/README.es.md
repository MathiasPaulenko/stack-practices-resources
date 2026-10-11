# Plantilla de Production Readiness Review — Recursos complementarios

Archivos companion de [Plantilla de Production Readiness Review](https://stackpractices.com/es/docs/production-readiness-review-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `production-readiness-review-template.md` | Checklist PRR rellenable en blanco — 10 dominios, notas de revisión y tabla de sign-off |
| `example-filled.md` | La revisión rellenada para un lanzamiento real (servicio de notificaciones, pase condicional con hallazgos rastreados) |

## Cómo usar

1. Copia `production-readiness-review-template.md` al wiki o repo de docs de tu equipo.
2. Circúlala a los revisores al menos una semana antes de la sesión.
3. Recorre los 10 dominios en orden; una casilla solo se marca con evidencia (enlace al dashboard, runbook, test).
4. Registra cada gap en Notas de Revisión con riesgo, responsable y fecha límite antes de terminar la reunión.
5. Recoge el sign-off por rol — ingeniería, producto, seguridad y SRE firman su propio dominio.
6. Decide: aprobado, condicional (lanzar con gaps rastreados) o rechazado (arreglar y reprogramar).
7. Mueve los hallazgos al issue tracker; trabajo sin asignar es trabajo sin terminar.

Compara con `example-filled.md` para calibrar la severidad de hallazgos y las decisiones de sign-off.
