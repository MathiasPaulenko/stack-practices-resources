# Plantilla de Política de Segmentación de Red — Recursos complementarios

Archivos descargables de la [Plantilla de Política de Segmentación de Red](https://stackpractices.com/es/docs/network-segmentation-policy-template/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `network-segmentation-policy.md` | Política en blanco rellenable: zonas, matriz de tráfico, controles, excepciones, roles. Cópiala en tu wiki o repo. |
| `reachability-validator.py` | Probador de alcance vía AWS SSM que verifica que el aislamiento entre zonas se cumple de verdad (sondas allow/deny entre subnets). |
| `calico-network-policies.yaml` | Dos manifiestos: un `NetworkPolicy` estándar de negación por defecto más un allow a nivel de carga de trabajo de Calico `projectcalico.org/v3`. |
| `segmentation-module.tf` | Módulo Terraform que crea un security group cuyas reglas de ingress/egress vienen enteras de variables: tu matriz de tráfico como código. |

## Uso

1. Rellena `network-segmentation-policy.md` empezando por la matriz de tráfico (deriva las filas de logs de flujo reales, no de suposiciones).
2. Aplica `calico-network-policies.yaml` en modo staged/log antes de imponerlo.
3. Adapta `segmentation-module.tf` a tu plan de CIDR; mantén las listas de `allowed_ingress`/`allowed_egress` alineadas con la matriz.
4. Ejecuta `reachability-validator.py` desde una instancia autorizada para confirmar que las denegaciones se mantienen, sobre todo tras cambios de reglas.
