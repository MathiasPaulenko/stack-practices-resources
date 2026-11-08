# Prevención de Deadlocks SQL — Simulación de Orden de Bloqueos

Ejemplos ejecutables de la receta [Prevención y Resolución de Deadlocks en Transacciones SQL](https://stackpractices.com/es/recipes/deadlock-prevention-sql/).

## Qué muestra

- **Adquisición sin orden**: dos transacciones bloquean filas en orden opuesto y caen en deadlock (detectado por timeout / ciclo de espera).
- **Adquisición ordenada**: ordenar los bloqueos elimina la espera circular — ambas transacciones terminan.
- **Reintento con jitter**: el patrón estándar para sobrevivir los deadlocks que igual ocurren bajo carga.

## Ejecutar

```bash
python src/deadlock_simulation.py
node src/deadlock-simulation.js
javac src/DeadlockSimulation.java && java -cp src DeadlockSimulation
```

Sin dependencias externas — Python y JavaScript usan solo la stdlib; Java usa `java.util.concurrent`.

## Relacionado

- Receta: <https://stackpractices.com/es/recipes/deadlock-prevention-sql/>
