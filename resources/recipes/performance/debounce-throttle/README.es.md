# Debounce y Throttle — Simulación de Ráfagas de Eventos

Ejemplos ejecutables de la receta [Debounce y Throttle](https://stackpractices.com/es/recipes/debounce-throttle/).

## Qué muestra

Una ráfaga de 12 eventos en 300ms más una cola de 3 eventos pasa por ambos limitadores:

- **Sin control**: cada evento dispara (15 ejecuciones).
- **Debounce** (espera de 250ms): dispara una vez por cada pausa — la ráfaga se reduce a un par de llamadas.
- **Throttle** (límite de 300ms): dispara como máximo una vez por ventana.

## Ejecutar

```bash
python src/debounce_throttle_simulation.py
node src/debounce-throttle-simulation.js
javac src/DebounceThrottleSimulation.java && java -cp src DebounceThrottleSimulation
```

Sin dependencias externas.

## Relacionado

- Receta: <https://stackpractices.com/es/recipes/debounce-throttle/>
