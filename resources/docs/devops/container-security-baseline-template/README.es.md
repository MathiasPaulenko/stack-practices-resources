# Plantilla de Línea Base de Seguridad de Contenedores — Código complementario

Manifiestos descargables para la [Plantilla de Línea Base de Seguridad de Contenedores](https://stackpractices.com/es/docs/container-security-baseline-template/) en StackPractices.

## Contenido

| Ruta | Qué contiene |
|------|--------------|
| `policies/kyverno-enforce-non-root.yaml` | ClusterPolicy que exige `runAsNonRoot` y `runAsUser` superior a 10000 |
| `policies/kyverno-disallow-privileged.yaml` | ClusterPolicy que rechaza contenedores privilegiados con el ancla condicional `=()` |
| `policies/kyverno-require-resources.yaml` | ClusterPolicy que exige requests y límites de CPU/memoria |
| `policies/namespace-pod-security.yaml` | Etiquetas de namespace que aplican `baseline` mientras avisan a nivel `restricted` |
| `network/default-deny-all.yaml` | NetworkPolicy que deniega todo el ingress y egress de un namespace |
| `network/allow-frontend-to-backend.yaml` | Regla explícita de ingress permitido entre dos cargas |
| `network/allow-dns-egress.yaml` | Regla de egress que permite DNS hacia kube-dns |
| `secrets/external-secret-registry.yaml` | ExternalSecret que sincroniza credenciales de registro desde un vault |
| `exceptions/exception-register.md` | Plantilla de registro de excepciones y aceptación de riesgo |

## Uso

1. Revisa cada archivo y ajusta namespaces, etiquetas, puertos y versiones fijadas a tu entorno.
2. Aplica las políticas primero en modo `Audit`/`warn`; cambia a `Enforce` tras corregir las violaciones.
3. Mantén el registro de excepciones en un lugar compartido y revísalo cada trimestre.

Consulta la página de la plantilla para la secuencia de despliegue, los pasos de verificación y el razonamiento detrás de cada control.
