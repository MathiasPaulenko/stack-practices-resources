# Ordenar un Array — Ejemplos Companion

Código companion de [Ordenar un Array](https://stackpractices.com/es/recipes/sort-array/).

Versiones ejecutables de las partes delicadas de la receta en tres lenguajes:

- **Ordenación multi-clave** — clave primaria más desempate determinista (tuplas, encadenamiento con `||`, `thenComparing`)
- **Ordenación numérica** — el pitfall `[10, 2].sort()` de JavaScript hecho bien
- **Manejo de nulos** — estrategias `nullsLast` que no crashean el comparador
- **Ordenación por locale** — `localeCompare` / `locale.strxfrm` para strings visibles al usuario

## Ejecutar

```bash
python -m pytest python/          # Tests Python
npx vitest run javascript/        # Tests JavaScript (vitest)
javac java/SortExamples.java && java -cp java SortExamples   # Demo Java
```
