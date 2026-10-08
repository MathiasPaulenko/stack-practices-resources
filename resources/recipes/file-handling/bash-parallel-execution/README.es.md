# Ejecución Paralela en Bash — Recursos Companion

Scripts ejecutables para la [receta de Ejecución Paralela en Bash](https://stackpractices.com/es/recipes/bash-parallel-execution/): fan-out/fan-in con `xargs -P`, pools de jobs en segundo plano con colección correcta de exit codes, y un semáforo contador para llamadas con límite de tasa.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `xargs-parallel.sh` | `xargs -P 4` sobre una lista de archivos con logs por job; reporta el exit 123 correctamente |
| `background-jobs.sh` | Pool de jobs con slots vía `wait -n` y `wait` por PID para exit codes reales |
| `semaphore.sh` | `sem` de GNU parallel limitando llamadas concurrentes (requiere GNU parallel) |

## Inicio rápido

```bash
mkdir -p input && touch input/{a,b,c,d,e,f}.txt
./xargs-parallel.sh            # 6 archivos, 4 a la vez
./background-jobs.sh           # 6 jobs, 3 slots — el job 3 falla a propósito
printf '1\n2\n3\n4\n5\n' > ids.txt
./semaphore.sh                 # necesita GNU parallel instalado
```

El script de jobs en segundo plano demuestra el patrón que la receta advierte no equivocar: `pids+=($!)` al lanzar, después `wait "$pid"` por job — nunca `wait` y luego `jobs -p`, que devuelve vacío una vez cosechados los jobs.
