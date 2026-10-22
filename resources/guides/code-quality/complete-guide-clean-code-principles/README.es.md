# Principios de Código Limpio — Companion antes/después

Ejercicio complementario de la guía [Principios de Código Limpio: Nombres, Funciones, Clases](https://stackpractices.com/es/guides/complete-guide-clean-code-principles/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `before/order-manager.ts` | Un `OrderManager` deliberadamente desordenado: función de 30 líneas, números mágicos, códigos de error, mutación oculta, nombres impronunciables |
| `after/order-processor.ts` | La misma lógica refactorizada: funciones pequeñas, colaboradores con SRP, constantes con nombre, excepciones, sin efectos secundarios |
| `eslint.config.mjs` | Reglas de ESLint que aplican los principios mecánicamente (`max-params`, `complexity`, `no-magic-numbers`, `max-depth`) |

## Ejercicio

1. Lee `before/order-manager.ts` y lista todos los olores que encuentres (apunta a al menos 8).
2. Refactorízalo tú mismo antes de abrir `after/`.
3. Compara tu versión con `after/order-processor.ts` —las diferencias son puntos de discusión, no una nota.
4. Ejecuta la config de lint sobre `before/` para ver qué olores atrapa una herramienta automáticamente:

```bash
npm install eslint
npx eslint before/ --config eslint.config.mjs
```

Las herramientas atrapan los olores mecánicos (tamaño, profundidad, números mágicos). Los semánticos —un nombre que miente, un efecto secundario que sorprende— siguen necesitando revisión humana.
