# Guía Completa de Seguridad de la Cadena de Suministro — Companion

Assets ejecutables de la [Guía Completa de Seguridad de la Cadena de Suministro](https://stackpractices.com/es/guides/complete-guide-supply-chain-security/) en StackPractices.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `sbom_validator.py` | Valida un SBOM CycloneDX: cumplimiento de licencias y componentes desactualizados |
| `typosquat_detector.py` | Marca paquetes cuyos nombres parecen typosquats/combosquats de paquetes populares |
| `generate_provenance.py` | Emite una atestación de procedencia SLSA v1.0 (declaración in-toto) |
| `secure-build.yml` | Workflow endurecido de GitHub Actions: actions fijadas por SHA, build aislado, firma + atestación |
| `sca-pipeline.yml` | Pipeline de Software Composition Analysis: pip-audit, npm audit, Trivy, Snyk, SBOM |
| `npmrc.example` | `.npmrc` que fija los paquetes con scope al registry interno (dependency confusion) |
| `pip.conf.example` | `pip.conf` con índice interno + fallback explícito; nota la opción de repo virtual |
| `requirements-hashed.txt` | `requirements.txt` de ejemplo con hashes (`pip install --require-hashes`) |

## Uso

```bash
# Validar un SBOM
python sbom_validator.py sbom.json

# Comprobar un nombre de paquete por typosquatting
python typosquat_detector.py reqeusts

# Escanear un requirements
python typosquat_detector.py --scan requirements.txt

# Generar una declaración de procedencia SLSA v1.0
python generate_provenance.py

# Copiar los workflows a tu repo
cp secure-build.yml .github/workflows/
cp sca-pipeline.yml .github/workflows/

# Aplicar las configs contra dependency confusion
cp npmrc.example .npmrc
cp pip.conf.example pip.conf
```

## Notas

- Los tres scripts `.py` solo usan la stdlib de Python.
- Los workflows fijan las actions de terceros a tags de release o SHAs completos — manténlo así.
- Para procedencia SLSA L3, invoca `slsa-github-generator` como reusable workflow a nivel de job (ver el job `provenance` comentado en `secure-build.yml`), nunca dentro de `steps`.
