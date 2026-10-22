# Laboratorio del Teorema CAP

Archivos complementarios de la guía [Teorema CAP y Trade-offs de Bases de Datos](https://stackpractices.com/es/guides/cap-theorem-guide/).

Un lab pequeño y ejecutable para ver el trade-off CP/AP en vez de solo leerlo: un clúster etcd de 3 nodos que puedes particionar con un script, más los snippets de ajuste de consistencia que la guía usa para PostgreSQL, Cassandra y MongoDB.

## Contenido

| Archivo | Qué muestra |
| ------- | ----------- |
| `docker-compose.yml` | Clúster etcd de 3 nodos (PC/EC — necesita quorum para escribir) |
| `simulate-partition.sh` | Corta/reconecta un nodo de la red del clúster, verifica quorum |
| `postgresql.conf` | Replicación síncrona: trade-off CP para Postgres |
| `notifications.cql` | Keyspace/tabla de Cassandra: setup AP con consistencia tunable |
| `mongo_consistency.js` | Ejemplos de `writeConcern` / `readConcern` / `readPreference` en MongoDB |

## Ejecutar el lab de particiones con etcd

```bash
docker compose up -d

# escribir a través del lado mayoritario
./simulate-partition.sh write

# aislar etcd3 — el lado minoritario
./simulate-partition.sh cut etcd3

# el lado mayoritario (etcd1+etcd2) mantiene quorum
./simulate-partition.sh status

# las escrituras al nodo aislado fallan: no hay quorum de su lado
docker exec etcd3 etcdctl put isolated-write nope   # timeout / error

# sanar y ver cómo se pone al día vía Raft
./simulate-partition.sh heal etcd3
```

Lo que acabas de ver: la partición mayoritaria sigue sirviendo porque conserva quorum (CP). El nodo aislado rechaza operaciones de consenso en lugar de divergir — disponibilidad sacrificada por consistencia.

Prueba de nuevo cortando dos nodos (`cut etcd2` y luego `cut etcd3`): ahora ningún lado tiene quorum y toda escritura falla. Eso es el teorema, no un bug.

## Adaptarlo

- Las particiones asimétricas requieren `iptables`/`tc` dentro de los contenedores — `docker network disconnect` solo produce un corte total.
- El mismo patrón del script funciona con un replica set de MongoDB o un clúster Cassandra multi-DC cambiando los servicios del compose.
- `simulate-partition.sh` usa el nombre de la red bridge de Docker; si el nombre de tu proyecto compose difiere, ajusta `NETWORK`.
