# Plantilla de Checklist de Despliegue — Recursos complementarios

Archivos descargables de la [Plantilla de Checklist de Despliegue](https://stackpractices.com/es/docs/deployment-checklist-template/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `deployment-checklist-template.md` | Checklist markdown en blanco que cubre pre-despliegue, despliegue y post-despliegue. Cópiala en tu wiki o repo y rellénala por release. |
| `example-filled.md` | La misma checklist rellenada para un release trabajado (`api-billing v2.4.0` con migración de esquema y feature flag). |
| `canary-deploy.sh` | Script de despliegue canary para Kubernetes + Istio VirtualService. Requiere `BUILD_TAG`; revierte automáticamente si la tasa de error del canary supera el 1%. |
| `deployment-communication.txt` | Plantilla de texto plano para narrar un despliegue en el canal del equipo, con timestamps y referencia de rollback. |

## Uso

1. Copia `deployment-checklist-template.md` en tu repo o wiki.
2. Rellena la tabla de metadatos y marca los ítems por release; elimina las secciones que no apliquen (p. ej. Base de Datos en cambios sin estado).
3. Adapta `canary-deploy.sh` a tu servicio, namespace y herramienta de tráfico (sustituye `virtualservice` por las anotaciones canary de tu ingress si no usas Istio).
4. Ten `deployment-communication.txt` abierto durante el despliegue y publica actualizaciones a medida que cada paso se completa.
