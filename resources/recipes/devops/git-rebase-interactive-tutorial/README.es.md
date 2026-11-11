# Rebase interactivo de Git — Demo de práctica

Código complementario de la receta de StackPractices:
https://stackpractices.com/es/recipes/git-rebase-interactive-tutorial/

## Qué contiene

| Archivo | Propósito |
|---|---|
| `demo.sh` | Construye un repo git de juguete (`rebase-demo/`) con 5 commits desordenados iguales a los ejemplos de la receta, y muestra una guía de práctica. |

## Cómo usarlo

1. Ejecuta `./demo.sh` — crea `rebase-demo/` con este historial:

```text
Fix typo in endpoint
Add debug logging
WIP: tests
WIP: fix validation
Add user model and API endpoints
```

2. Haz `cd rebase-demo` y ejecuta `git rebase -i HEAD~5`.
3. Practica cada acción sobre commits reales:
   - **split** — `edit` en "Add user model and API endpoints", luego `git reset HEAD^` y commitea el modelo y los endpoints por separado.
   - **squash** — `squash` en los dos commits WIP para fusionarlos con el primero.
   - **drop** — `drop` en "Add debug logging".
   - **reword** — `reword` en "Fix typo in endpoint".
4. Prueba también el flujo autosquash: `git commit --fixup <sha>` y luego `git rebase -i --autosquash HEAD~5`.
5. `./demo.sh --cleanup` elimina el repo de práctica.

Requisitos: git 2.32+ (para `--fixup=amend:` / `--fixup=reword:`), bash.
