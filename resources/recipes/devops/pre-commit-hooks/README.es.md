# Pre-Commit Hooks — Ejemplos Ejecutables

Código companion de la receta de StackPractices:  
https://stackpractices.com/es/recipes/pre-commit-hooks/

## Contenido

| Archivo | Propósito |
|---|---|
| `.pre-commit-config.yaml` | Framework `pre-commit` de Python con black, flake8, mypy y gitleaks |
| `package.json` | Configuración Node para husky, lint-staged, simple-git-hooks y commitlint |
| `.husky/pre-commit` | Hook pre-commit de Husky v9 |
| `.lintstagedrc.js` | Config de lint-staged para JS/TS y JSON/Markdown/YAML |
| `commitlint.config.js` | Reglas de conventional commits |
| `build.gradle` | Verificación de formateo Spotless para Java/Gradle |
| `lefthook.yml` | Config del gestor de hooks multi-lenguaje |
| `.gitattributes` | Finales de línea LF para scripts shell |

## Cómo usar

### Python

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Node con husky

```bash
npm install
npx husky init
```

Reemplazá `.husky/pre-commit` con el ejemplo de este repo.

### Node con simple-git-hooks

```bash
npm install
npx simple-git-hooks
```

### Java con Gradle

```bash
./gradlew spotlessCheck
# Para corregir el formateo:
# ./gradlew spotlessApply
```

### Multi-lenguaje con lefthook

```bash
lefthook install
lefthook run pre-commit
```

## No hagas commit directamente en `.git/hooks`

Los scripts de hook mismos viven en `.git/hooks/` y no se rastrean. Los archivos de configuración de este repo sí están rastreados y se usan con las herramientas de arriba para instalar los hooks automáticamente.

## Licencia

MIT — usalo bajo tu propia responsabilidad en tus proyectos.
