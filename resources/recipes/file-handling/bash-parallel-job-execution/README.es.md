# Control de Jobs Paralelos en Bash — Ejemplos Companion

Scripts de control de jobs ejecutables, companion de la
[receta Control de Jobs Paralelos](https://stackpractices.com/es/recipes/bash-parallel-job-execution/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `job-control.sh` | Wrapper de GNU parallel: joblog, timeout por job, cortacircuitos `--halt`, resumen + lista de fallidos |
| `xargs-exit-codes.sh` | Archivos de resultado por job con `xargs -P` cuando parallel no está instalado |
| `retry-backoff.sh` | Reintentos con backoff exponencial y timeout por intento |
| `parallel_pool.py` | El mismo control de forma nativa en Python con `multiprocessing.Pool` |

## Inicio rápido

```bash
# Crear un archivo de input de demo
printf 'task-a\ntask-b\ntask-c\n' > jobs.txt

# Wrapper GNU parallel — requiere: apt install parallel
./job-control.sh 4 jobs.txt

# Variante xargs — sin dependencias extra
./xargs-exit-codes.sh 4 jobs.txt

# Reintentos — requiere GNU parallel
./retry-backoff.sh 4 3 60 jobs.txt

# Python — jobs.txt debe contener comandos de shell completos
printf 'echo a && sleep 1\necho b && sleep 1\n' > jobs.txt
python parallel_pool.py
```

## Advertencias

- `xargs -I {}` **no** soporta la sintaxis `{//}` de GNU parallel — usá `basename` dentro del wrapper `sh -c`, como se muestra.
- `--resume` / `--resume-failed` solo funcionan con un joblog de una corrida previa.
- `retry-backoff.sh` re-ejecuta tareas; usalo solo para jobs idempotentes.
