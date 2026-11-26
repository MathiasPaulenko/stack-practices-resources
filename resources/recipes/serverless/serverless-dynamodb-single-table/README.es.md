# Diseño Single-Table en DynamoDB — Archivos de apoyo

Proyecto ejecutable complementario de la [receta de diseño single-table en DynamoDB](https://stackpractices.com/es/recipes/serverless-dynamodb-single-table/) en StackPractices.

- `access-patterns.txt` — los ocho access patterns y el layout de entidades sobre los que se diseña el schema. Lista los tuyos antes de escribir código.
- `create_table.py` — llamada a `create_table` con claves compuestas `PK`/`SK` y un `GSI1` sobrecargado (`PAY_PER_REQUEST`).
- `entities.py` — escritores para `User`, `Order` (dos particiones: header + copia índice), `OrderItem` y `Product`.
- `queries.py` — implementación de los ocho access patterns, incluyendo `begins_with`, `get_item` directo y queries sobre el GSI.
- `transactions.py` — `transact_write_items` para crear una orden con sus items de forma atómica, y un update de dos items que mueve el status en ambas copias.
- `gsi_variants.py` — GSI sparse (los drafts quedan fuera del índice) y prefijos de GSI sobrecargado.
- `pagination.py` — paginación por cursor con `ExclusiveStartKey` / `LastEvaluatedKey`.

Requiere `boto3` y credenciales de AWS (o apunta boto3 a DynamoDB Local).
