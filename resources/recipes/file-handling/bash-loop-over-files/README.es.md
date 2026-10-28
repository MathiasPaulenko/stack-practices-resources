# Loop sobre Archivos en Bash — Recursos Complementarios

Scripts ejecutables para la receta [Cómo Iterar sobre Archivos en Bash](https://stackpractices.com/es/recipes/bash-loop-over-files/): loops seguros con glob, pipelines `find -print0`, renombrado por lotes, arrays con `mapfile`, lotes con `xargs` e iteración ordenada por fecha.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `loop-glob.sh` | Loop básico `for file in *.txt` con guarda `[ -e ]` para no-coincidencias |
| `find-print0-loop.sh` | `while IFS= read -r -d ''` recursivo sobre `find -print0` — sobrevive espacios y saltos de línea |
| `bulk-rename.sh` | Renombrado por lotes `.jpeg` → `.jpg` con `nullglob` y `mv --` |
| `mapfile-read.sh` | Lectura de una lista grande de archivos a un array con `mapfile -d ''` |
| `xargs-batch.sh` | Procesamiento por lotes en paralelo con `xargs -0 -P 4` |
| `sort-by-mtime.sh` | Itera archivos del más reciente al más antiguo con `find -printf` + `sort -z` |

## Inicio rápido

```bash
mkdir -p demo && cd demo
touch {a,b,c}.txt "file with spaces.txt" report_{003,001,002}.txt

../loop-glob.sh            # cuenta archivos .txt, no se salta ninguno
../find-print0-loop.sh .   # lista todos los archivos, espacios incluidos
```

Los scripts siguen las reglas que enseña la receta: entrecomilla cada expansión, prefiere `find -print0` sobre `ls`, activa `nullglob` cuando un glob puede no tener coincidencias y recolecta la lista antes de modificar archivos.
