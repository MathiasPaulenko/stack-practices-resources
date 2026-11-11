# Flujo de trabajo Git en equipo — Demo de práctica

Archivos complementarios de la receta de StackPractices
[Flujo de trabajo Git: ramas, pull requests e historial limpio](https://stackpractices.com/es/recipes/git-workflow/).

## Archivos

- `demo.sh` — construye un repositorio desechable (`git-workflow-demo/`) y ejecuta
  el ciclo completo de GitHub Flow que muestra la receta.

## Qué cubre la demo

1. Inicializa un repo en `main` (la rama protegida en el mundo real).
2. Crea una rama `feature/login` con dos Conventional Commits.
3. Hace squash-merge de vuelta a `main` — cómo se ve el merge de un PR.
4. Crea el tag `v1.0.0` como release.
5. Corrige un bug en `release/1.0.x` y hace cherry-pick del hotfix de vuelta a `main`.

## Uso

```bash
chmod +x demo.sh
./demo.sh
```

El script deja un directorio `git-workflow-demo/` que puedes inspeccionar
(`git log`, `git branch`, `git tag`) y borrar cuando termines.

## Requisitos

- Bash (Git Bash en Windows funciona)
- Git 2.x
