# Plantilla de Política de Auto-Scaling — Recursos descargables

Assets listos para usar de la [Plantilla de Política de Auto-Scaling](https://stackpractices.com/es/docs/auto-scaling-policy-template/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `auto-scaling-policy-template.md` | El documento de política listo para copiar — rellena el encabezado `<Service Name>` y ajusta los umbrales |
| `autoscaling.tf` | Terraform: AWS Auto Scaling Group con políticas de scale-up/scale-down y alarmas de CloudWatch |
| `hpa.yaml` | HorizontalPodAutoscaler de Kubernetes (autoscaling/v2) con métricas de CPU, memoria y RPS personalizada |
| `scaling-events-example.txt` | Formato de ejemplo de log de eventos de escalamiento para dashboards y auditorías |

## Uso

1. Copia `auto-scaling-policy-template.md` a la documentación de tu equipo y completa los metadatos del servicio.
2. Adapta `autoscaling.tf` o `hpa.yaml` a tu plataforma — elige umbrales según tu warm-up medido, no los valores por defecto.
3. Prueba la política con carga en staging antes de activarla en producción (ver la sección *Adopción de esta política* del documento).
