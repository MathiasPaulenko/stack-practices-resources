# Elasticsearch Cluster Setup — Production Configs

Companion resources for the guide [Complete Guide to Elasticsearch Cluster Setup](https://stackpractices.com/guides/complete-guide-elasticsearch-cluster-setup/).

## Files

| File | What it is |
| --- | --- |
| `elasticsearch.yml` | Commented 3-node production config (master+data nodes, security, memory lock, disk watermarks). Change `node.name` per host; remove `cluster.initial_master_nodes` after first bootstrap. |
| `docker-compose.yml` | 3-node ES 8.15 test cluster on a private network — security enabled, `elastic` password via env var, HTTP on 9200 for local `curl`. Not a production recipe. |
| `ilm-policy.json` | hot/warm/cold/delete lifecycle for `logs-*` indices (rollover 7d/50GB → shrink+forcemerge at 30d → cold nodes at 90d → delete at 365d). |
| `index-template.json` | Settings + mappings + ILM hookup for `logs-*` — where index defaults live in ES 8. |

## Usage

```bash
# Local test cluster
docker compose up -d
curl -u elastic:$ELASTIC_PASSWORD http://localhost:9200

# Apply template and policy (order matters: policy first)
curl -u elastic:$ELASTIC_PASSWORD -XPUT http://localhost:9200/_ilm/policy/logs-policy \
  -H 'Content-Type: application/json' -d @ilm-policy.json
curl -u elastic:$ELASTIC_PASSWORD -XPUT http://localhost:9200/_index_template/logs \
  -H 'Content-Type: application/json' -d @index-template.json
```

## Gotchas

- `cluster.initial_master_nodes` is **bootstrap-only** — remove it after the cluster forms.
- `bootstrap.memory_lock: true` fails without `vm.max_map_count >= 262144` and a proper fd limit on the host.
- The old ILM `freeze` action is deprecated in ES 8 — cold phase uses `allocate` or searchable snapshots.
- Index-level defaults (`index.*`) don't exist as node settings in ES 8; they live in the index template.
