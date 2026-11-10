# Plantilla de Configuración de Entornos — Recursos complementarios

Plantilla de documentación rellenable para capturar variables de entorno, endpoints, ajustes de infraestructura y ubicaciones de secretos por entorno de despliegue.

## Archivos

- `environment-configuration-template.md` — plantilla en blanco con las seis secciones
- `configmap-secret-example.yaml` — manifiesto de ConfigMap + Secret en Kubernetes mostrando la división sensible/no sensible
- `secret-rotation-schedule.txt` — esqueleto de calendario de rotación
- `example-filled.md` — la plantilla rellenada para un servicio de pagos ficticio

## Uso

Copia `environment-configuration-template.md` en el repositorio o wiki de tu servicio, rellena cada fila de las tablas por entorno y actualízala en el mismo PR que cualquier cambio de configuración. Nunca guardes valores de secretos reales — registra rutas del vault en su lugar.

Fuente: https://stackpractices.com/es/docs/environment-configuration-template/
