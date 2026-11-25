# Checklist de Debugging de Race Conditions — Companion

Reproducciones y soluciones ejecutables del
[checklist de debugging de race conditions](https://stackpractices.com/es/docs/race-condition-debugging-checklist/).
Cada archivo corresponde a una sección del checklist: dispara la race,
mira cómo la reporta el detector y verifica que la solución la silencia.

## Archivos

| Archivo | Lenguaje | Sección del checklist | Qué hace |
|---------|----------|-----------------------|----------|
| `stress_counter.py` | Python | 2.1 | Machaca un contador no atómico desde 100 threads; un conteo corto son updates perdidos |
| `barrier_repro.py` | Python | 2.2 | `threading.Barrier` fuerza dos threads a arrancar a la vez: interleaving determinista |
| `RaceConditionStress.java` | Java (jcstress) | 2.3 | Test del modelo de memoria; el resultado "0, 0" está prohibido: una ejecución real, no teoría |
| `counter_race.go` | Go | 3.2 | Incremento sin sincronizar; corre con `go run -race` para ver el reporte |
| `counter_fix.go` | Go | 4.2 / 5.1 | El mismo contador tras un mutex; `-race` queda en silencio |

## Ejecución

```bash
python stress_counter.py        # espera "LOST n updates" en la mayoría de ejecuciones
python barrier_repro.py         # imprime cuántas veces el lector no vio la escritura
go run -race counter_race.go    # WARNING: DATA RACE con dos stacks
go run -race counter_fix.go     # limpio; siempre 100000
# RaceConditionStress.java necesita el harness de jcstress:
# https://openjdk.org/projects/code-tools/jcstress/
```

## Notas

- `stress_counter.py` y `barrier_repro.py` solo necesitan Python 3.8+.
- `counter_*.go` necesita Go 1.20+; el flag `-race` requiere CGO habilitado.
- Las races dependen del timing: una ejecución limpia no prueba nada. Repite
  las reproducciones en loop, ejecútalas bajo un race detector y trata cada
  interleaving reportado como un bug real.
