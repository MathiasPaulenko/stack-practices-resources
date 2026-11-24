# Análisis estático con Bandit — archivos de apoyo

Archivos de la receta
[Encontrar problemas de seguridad en código Python con Bandit](https://stackpractices.com/es/recipes/python-bandit-static-analysis/).

| Archivo | Propósito |
| --- | --- |
| `bandit.ini` | Config `.bandit` en la raíz: solo exclusiones de rutas, todas las reglas activas. |
| `pyproject.toml` | Alternativa TOML (`[tool.bandit]`); cargar con `bandit -c pyproject.toml -r src/`. |
| `pre-commit-config.yaml` | Hook de pre-commit fijado a una versión publicada de Bandit. |
| `bandit-workflow.yml` | Job de GitHub Actions que falla según el umbral de gravedad y sube el informe JSON. |
| `bandit_plugins/no_print_statements.py` | Check personalizado registrado vía el grupo `bandit.plugins`. |

## Notas

- El baseline se genera en tu propio repo: `bandit -r src/ -f json -o .bandit-baseline.json --exit-zero`, luego `bandit -r src/ -b .bandit-baseline.json`.
- Los plugins deben ser importables en el entorno donde corre Bandit: empaquétalos e instálalos; no pases rutas de archivo a la CLI.
