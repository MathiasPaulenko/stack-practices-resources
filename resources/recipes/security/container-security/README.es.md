# Seguridad de contenedores — artefactos ejecutables

Recursos complementarios de [Seguridad de contenedores: escanea, endurece y firma imágenes Docker](https://stackpractices.com/es/recipes/container-security/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `Dockerfile` | Build multi-stage endurecido — runtime distroless, uid no-root 65532 |
| `Dockerfile.alpine` | Alternativa con shell (`dumb-init` + usuario propio) |
| `security-scan.yml` | Control en GitHub Actions: escaneo Trivy, subida SARIF, artefacto SBOM, reescaneo semanal |
| `.gitlab-ci.yml` | Equivalente en GitLab CI |
| `trivy.yaml` | Configuración del escáner — umbral de severidad, ignore-unfixed, directorios omitidos |
| `.trivyignore` | Plantilla de excepciones de CVEs revisados con justificación |
| `k8s-deployment.yaml` | securityContext de pod blindado (raíz solo lectura, sin capabilities, seccomp) |
| `kyverno-policy.yaml` | Control de admisión — solo corren imágenes firmadas con Cosign |
| `scan.sh` | Pipeline local: build → Trivy → TruffleHog → Syft → Grype → Cosign |

## Inicio rápido

```bash
# Escanea una imagen local (falla con HIGH/CRITICAL que tengan parche)
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 myapp:latest

# Pipeline local completo
chmod +x scan.sh && ./scan.sh myapp:latest

# Despliega con el contexto endurecido (sustituye el digest primero)
kubectl apply -f k8s-deployment.yaml
```

Requiere: Docker, Trivy, Syft, Grype, Cosign, TruffleHog.
