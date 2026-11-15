# Topic Request

Copy this template into your ticketing system when requesting a new Kafka topic.

## Requested name

`env.domain.entity.event-type[.version]` — e.g. `prod.orders.order-created.v1`

## Details

| Field | Value |
|---|---|
| Topic name | |
| Expected throughput (msg/s) | |
| Expected message size (KB) | |
| Retention required | |
| Partition count (+ justification) | |
| Owning team | |
| Consumer teams / groups | |
| Compaction needed? | yes / no |

## Checklist

- [ ] Name passes `naming-lint.sh`
- [ ] Domain exists in the domain registry (or proposal submitted)
- [ ] Partition count justified by consumer parallelism
- [ ] Retention agreed with consuming teams
- [ ] ACL principals identified
