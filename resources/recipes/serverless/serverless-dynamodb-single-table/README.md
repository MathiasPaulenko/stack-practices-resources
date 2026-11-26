# DynamoDB Single-Table Design — Companion Files

Runnable companion for the [DynamoDB single-table recipe](https://stackpractices.com/recipes/serverless-dynamodb-single-table/) on StackPractices.

- `access-patterns.txt` — the eight access patterns and entity layout the schema is designed around. List yours before writing code.
- `create_table.py` — `create_table` call with composite `PK`/`SK` and one overloaded `GSI1` (`PAY_PER_REQUEST`).
- `entities.py` — writers for `User`, `Order` (two partitions: header + index copy), `OrderItem` and `Product`.
- `queries.py` — implementations for all eight access patterns, including `begins_with`, direct `get_item` and GSI queries.
- `transactions.py` — `transact_write_items` to create an order with its items atomically, and a two-item update that moves status on both copies.
- `gsi_variants.py` — sparse GSI (drafts excluded from the index) and overloaded GSI prefixes.
- `pagination.py` — cursor pagination with `ExclusiveStartKey` / `LastEvaluatedKey`.

Requires `boto3` and AWS credentials (or point boto3 at DynamoDB Local).
