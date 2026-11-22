# Guía de Monolito Modular — Código complementario

Una implementación ejecutable y sin dependencias del enforcement de límites descrito en la [guía de Monolito Modular](https://stackpractices.com/es/guides/modular-monolith-guide/): un linter que recorre un árbol `modules/`, resuelve cada import y reporta cualquier módulo que meta la mano en las internas de otro en vez de su `api` pública.

## Archivos

| Archivo | Stack | Tests |
|---------|-------|-------|
| `boundary_check.py` | Python stdlib (`re`, `pathlib`, `unittest`) | 4 casos unittest |
| `boundary_check.mjs` | Node.js (`node:test`, `node:assert`, `node:fs`) | 4 casos con `node --test` |

## Ejecutar

```bash
# Suites de tests
python -m unittest boundary_check -v
node --test boundary_check.mjs

# Lint sobre un codebase real (la versión Python también funciona como CLI)
python boundary_check.py /ruta/a/tu-proyecto
```

## La regla que fuerza

- `modules/<nombre>/api/` es la única superficie pública — otros módulos pueden importarla.
- `shared/kernel/` es compartido por todos, en ambas direcciones.
- Cualquier import que cruza la línea de un módulo hacia `domain/`, `application/` o `infrastructure/` es una violación: se reporta el archivo, la línea y el import ofensor.

## Por qué un test y no una convención

Un límite que solo vive en una guía de estilo se erosiona en meses — alguien con deadline importa el repositorio de otro módulo "solo esta vez". Un check de CI que falla convierte el "por favor no" en "no se puede mergear", que es exactamente el punto del patrón.
