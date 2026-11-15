# Balanceo de carga con HAProxy — Código complementario

Ejemplos ejecutables que acompañan a la receta [Balanceo de carga con HAProxy y health checks](https://stackpractices.com/es/recipes/load-balancing-haproxy/) de StackPractices.

La demo simula la máquina de estados de los health checks detrás de `default-server inter 5s fall 2 rise 3`: un backend cae a DOWN tras dos fallos consecutivos y solo vuelve tras tres aciertos seguidos, mientras un dispatcher `leastconn` reparte las peticiones entre los servidores activos.

Tres backends durante 20 intervalos de sondeo:

- **web1** — sano en toda la ejecución
- **web2** — falla en t=0..3 (DOWN en t=1), se recupera en t=6 y vuelve a recibir tráfico
- **web3** — alterna `ok/fail/fail` para siempre; nunca logra tres aciertos seguidos, así que permanece DOWN aunque responda algunas sondas

Salida esperada (idéntica en los tres lenguajes):

```text
web2: DOWN after 2 fails
web2: UP after 3 passes
web3: DOWN after 2 fails

Requests served per backend (of 20):
  web1: 10
  web2: 9
  web3: 1
```

## Ejecutar

```bash
python health_check_fsm.py
node health-check-fsm.js
javac HealthCheckFsm.java && java HealthCheckFsm
```

## Archivos

| Archivo | Demo |
|---|---|
| `health_check_fsm.py` | FSM fall/rise + dispatch leastconn (Python) |
| `health-check-fsm.js` | Misma simulación (Node.js) |
| `HealthCheckFsm.java` | Misma simulación (Java) |
