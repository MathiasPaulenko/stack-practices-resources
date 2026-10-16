# Plantilla de Seguridad de Red

Plantilla de inventario de seguridad de red más los scripts de automatización del artículo: un auditor de security groups, un analizador de flow logs de VPC, NetworkPolicies base para Kubernetes y un verificador de default-deny.

Artículo fuente: [Plantilla de Documentación de Seguridad de Red](https://stackpractices.com/es/docs/network-security-template/)

## Archivos

- `network-security-inventory.md` — la plantilla de inventario en blanco, lista para copiar en tu runbook
- `sg_audit.py` — audita todas las reglas de security groups y exporta un informe CSV/JSON con severidad (`critical` para `0.0.0.0/0` en entrada en puertos no web, `warning` en caso contrario)
- `flow_log_analysis.sh` — consulta los flow logs de VPC en busca de tráfico rechazado y ordena las IPs que escanean tu red
- `k8s-networkpolicies.yaml` — baseline de NetworkPolicies: default-deny + egress DNS + frontend-a-backend
- `check_default_deny.sh` — falla si algún namespace no tiene una NetworkPolicy default-deny

## Cómo usarlo

1. Copia `network-security-inventory.md` y rellena cada sección desde la configuración real: la tabla «Cómo Rellenar Cada Sección» del artículo mapea cada fila al comando que la produce.
2. Ejecuta `python sg_audit.py --region us-east-1` para una auditoría puntual de security groups; adjunta el CSV a tu revisión.
3. Ejecuta `./flow_log_analysis.sh /aws/vpc/flow-logs` para detectar intentos de escaneo y movimiento lateral.
4. Aplica `k8s-networkpolicies.yaml` por namespace y verifica la cobertura con `./check_default_deny.sh`.

## Requisitos

- `sg_audit.py`: Python 3.9+, `boto3`, credenciales con `ec2:DescribeSecurityGroups`
- `flow_log_analysis.sh`: AWS CLI, acceso de lectura a CloudWatch Logs, flow logs de VPC activados
- Scripts de Kubernetes: `kubectl`, `jq`, un CNI que aplique NetworkPolicy (Cilium, Calico)
