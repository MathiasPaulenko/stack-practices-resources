# Checklist de Hardening de Imágenes Docker — Archivos complementarios

Archivos ejecutables del [Checklist de Hardening de Imágenes Docker](https://stackpractices.com/es/docs/docker-image-hardening-checklist/) de StackPractices.

## Qué incluye

| Archivo | Propósito |
| --- | --- |
| `Dockerfile` | Build multi-etapa Node endurecido: UID 1001 no-root, montaje de secreto BuildKit, capas limpias |
| `.dockerignore` | Exclusiones de contexto — secretos, `.git`, node_modules, docs |
| `docker-compose.hardened.yml` | Hardening completo en runtime: rootfs read-only, `cap_drop: ALL`, tmpfs, aislamiento de red, límites, secretos |
| `seccomp-profile.json` | Perfil seccomp de lista blanca para una app Node |
| `trivy-scan.yml` | Pipeline GitHub Actions: build → barrera Trivy (HIGH/CRITICAL) → SBOM → firma Cosign |
| `run-hardened.sh` | `docker run` con todos los controles de runtime |
| `verify-hardening.sh` | Comandos de verificación — cada check debe pasar o fallar cerrado |
| `src/server.js`, `package.json` | App mínima para que la imagen compile y corra de verdad |
| `secrets/db-password.txt` | Secreto de runtime de ejemplo (reemplazar, nunca commitear valores reales) |

## Inicio rápido

```bash
# 1. Compilar la imagen endurecida
docker build -t myapp:hardened -f Dockerfile .

# 2. Crear la red backend y ejecutar endurecido
docker network create backend --internal
./run-hardened.sh

# 3. Verificar cada control
./verify-hardening.sh myapp

# O usar el stack de compose
docker compose -f docker-compose.hardened.yml up --build
```

## Escanear y firmar

```bash
trivy image myapp:hardened --severity HIGH,CRITICAL --exit-code 1
trivy image --format cyclonedx --output sbom.json myapp:hardened
cosign sign --yes myapp:hardened
```
