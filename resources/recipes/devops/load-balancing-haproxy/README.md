# Load Balancing with HAProxy — Companion Code

Runnable companions to the [Load Balancing with HAProxy and Health Checks](https://stackpractices.com/recipes/load-balancing-haproxy/) recipe on StackPractices.

The demo simulates the health-check state machine behind `default-server inter 5s fall 2 rise 3`: a backend goes DOWN after two consecutive probe failures and rejoins only after three consecutive passes, while a `leastconn` dispatcher routes requests across the servers currently up.

Three backends over 20 probe intervals:

- **web1** — healthy the whole run
- **web2** — fails at t=0..3 (DOWN at t=1), recovers at t=6 and starts receiving traffic again
- **web3** — flaps `ok/fail/fail` forever; it never earns three consecutive passes, so it stays DOWN despite answering some probes

Expected output (identical in all three languages):

```text
web2: DOWN after 2 fails
web2: UP after 3 passes
web3: DOWN after 2 fails

Requests served per backend (of 20):
  web1: 10
  web2: 9
  web3: 1
```

## Run

```bash
python health_check_fsm.py
node health-check-fsm.js
javac HealthCheckFsm.java && java HealthCheckFsm
```

## Files

| File | Demo |
|---|---|
| `health_check_fsm.py` | fall/rise FSM + leastconn dispatch (Python) |
| `health-check-fsm.js` | Same simulation (Node.js) |
| `HealthCheckFsm.java` | Same simulation (Java) |
