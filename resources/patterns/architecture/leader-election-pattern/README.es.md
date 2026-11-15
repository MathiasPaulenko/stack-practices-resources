# Patrón de Elección de Líder — Código complementario

Implementaciones ejecutables del recurso [Patrón de Elección de Líder](https://stackpractices.com/es/patterns/leader-election-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `leader_election.py` | Demo autocontenida: almacén CAS atómico + fencing tokens, con caída y conmutación simuladas. Corre con Python 3 sin servicios. |
| `leader-election-etcd.py` | Elección sobre `client.transaction` de etcd con lease TTL (python-etcd3). Requiere etcd en `localhost:2379`. |
| `leader-election-redis.py` | Adquisición con `SET clave token NX PX` + compare-and-delete / compare-and-renew en Lua. Requiere Redis en `localhost:6379`. |
| `leader-election-k8s.go` | Bucle de actualización de client-go contra la API `Lease` de Kubernetes. |
| `lease.yaml` | Manifiesto `coordination.k8s.io/v1` en crudo para `kubectl apply -f`. |

## Inicio rápido

```bash
python leader_election.py
```

Salida esperada: `node-1` gana el lease, lo renueva dos veces, cae, y una
seguidora toma el control con un fencing token mayor.

Para las variantes de etcd y Redis, levanta primero el servicio:

```bash
docker run -d -p 2379:2379 gcr.io/etcd-development/etcd:v3.5.11
pip install etcd3 && python leader-election-etcd.py

docker run -d -p 6379:6379 redis:7
pip install redis && python leader-election-redis.py
```

## Por qué importan los fencing tokens

Cada implementación devuelve o porta un token monótono (`fence` en
`leader_election.py`, `mod_revision` en etcd, el valor del token en Redis).
Los servicios downstream deben rechazar escrituras con un token menor —
es la única forma fiable de impedir que un ex-líder pausado o particionado
siga escribiendo como si estuviera al mando.
