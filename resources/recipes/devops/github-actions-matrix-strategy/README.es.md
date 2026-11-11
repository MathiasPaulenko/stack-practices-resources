# Matrix de GitHub Actions — Workflows ejecutables

Archivos complementarios de la receta de StackPractices
[github-actions-matrix-strategy](https://stackpractices.com/es/recipes/github-actions-matrix-strategy/).

Copia `.github/` en un repositorio Node.js y haz push: los workflows generan jobs de matrix reales que puedes ver en la pestaña Actions.

## Archivos

| Archivo | Qué demuestra |
|---|---|
| `.github/workflows/matrix-static.yml` | Matrix 3×3 de SO × Node con `exclude`, `include` (celda extra de coverage), `fail-fast: false`, nombres de job y claves de caché por celda |
| `.github/workflows/matrix-services.yml` | Matrix de contenedores de servicio: PostgreSQL y MySQL vía config transportada por `include` |
| `.github/workflows/matrix-dynamic.yml` | Un job `prepare` emite el eje desde `supported-versions.json`; guarda anti-array-vacío para que un archivo roto falle a las claras |
| `.github/supported-versions.json` | Fuente única de verdad del eje dinámico: edítalo y la matrix lo sigue |

## Uso

```bash
# Copiar a cualquier repo Node.js
cp -r .github /ruta/a/tu/repo/

# Push — los tres workflows aparecen en la pestaña Actions
```

Los workflows asumen que `npm ci` + `npm test` funcionan. Sustituye por tus propios comandos si tu repo usa otro stack: la mecánica de matrix es agnóstica al lenguaje.
