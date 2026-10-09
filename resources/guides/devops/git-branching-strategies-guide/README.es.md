# Estrategias de Branching en Git — Recursos complementarios

Archivos complementarios de [Estrategias de Branching en Git Comparadas](https://stackpractices.com/es/guides/git-branching-strategies-guide/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `branch-protection-rules.json` | Payload de la API de GitHub: checks obligatorios, revisiones, historia lineal, sin force pushes para `main` y `develop` |
| `github-flow-ci.yml` | Gate CI de GitHub Actions — tests + lint obligatorios antes del merge a `main` (GitHub Flow / trunk-based) |

## Cómo usarlo

1. Aplica las reglas de protección: `PUT /repos/{owner}/{repo}/branches/{branch}/protection` con el payload JSON (o recréalas en Settings → Branches del repo).
2. Copia `github-flow-ci.yml` a `.github/workflows/` y adapta los nombres de jobs a tu stack.

La estrategia solo funciona si los gates se aplican — las reglas de protección y los checks obligatorios son la capa de enforcement.