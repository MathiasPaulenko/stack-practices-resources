# Graph Databases (Neo4j) — Companion Files

Every Cypher example from the guide as runnable scripts, plus a `docker-compose.yml`
that brings up Neo4j 5 with the Graph Data Science plugin — the fastest way to
run everything without installing anything else.

Source guide: <https://stackpractices.com/guides/graph-database-guide/>

## Files

| File | Contents |
|------|----------|
| `docker-compose.yml` | Neo4j 5 + GDS plugin; UI on `localhost:7474`, Bolt on `7687` |
| `01-cypher-basics.cypher` | CREATE, variable-length `*2` traversal, `shortestPath` |
| `02-recommendation-engine.cypher` | Collaborative filtering: buyers of X also bought Y |
| `03-fraud-detection.cypher` | Circular transfer detection with `*3..5` paths |
| `04-access-control.cypher` | Nested group membership check via `*0..` |
| `05-hierarchies.cypher` | Org chart and category tree traversals |
| `06-social-network-model.cypher` | Labels, relationship types, indexes, unique constraint |
| `07-social-network-queries.cypher` | Degrees of separation, recommendations, Louvain, complementary skills |

## Run

```bash
docker compose up -d
# open http://localhost:7474  (user: neo4j / pass: testpassword)
```

Then paste any `.cypher` file into the browser editor, or pipe it through
`cypher-shell`:

```bash
cat 01-cypher-basics.cypher | docker exec -i stackpractices-neo4j \
  cypher-shell -u neo4j -p testpassword
```

## Notes

- Variable-length traversals are bounded (`*2`, `*3..5`) on purpose. Removing
  the bounds on a dense graph is the classic way to blow the heap.
- `07-social-network-queries.cypher` uses the GDS library (`gds.louvain`),
  which is already enabled in the compose file via `NEO4J_PLUGINS`.
- The sample queries assume nodes with the properties used in the guide
  (`name`, `email`, `location`, …). Create them with `01-cypher-basics.cypher`
  or your own seed data first.
