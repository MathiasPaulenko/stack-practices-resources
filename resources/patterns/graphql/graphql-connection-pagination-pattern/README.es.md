# Patrón de Paginación Connection en GraphQL

Ejemplos ejecutables del patrón de StackPractices
[Patrón de Paginación Connection en GraphQL](https://stackpractices.com/es/patterns/graphql-connection-pagination-pattern/).

Dos implementaciones de resolver que paginan la misma tabla en memoria de 95
usuarios con la salida completa de `edges` / `pageInfo` / `totalCount`:

| Archivo | Payload del cursor | Qué muestra |
| --- | --- | --- |
| `offset-cursor.mjs` | `base64("offset:N")` | El cursor de offset clásico: simple, correcto y suficiente para tablas pequeñas. El truco del `LIMIT + 1` responde `hasNextPage` sin consulta de conteo. |
| `keyset-cursor.mjs` | `base64("created_at:id")` | Paginación keyset / clave de orden: el cursor lleva los valores de orden de la última fila, así la base de datos salta con `WHERE (created_at, id) < ($1, $2)` en lugar de escanear filas de `OFFSET`. |

## Requisitos

- Node.js 18+. **Sin dependencias**: ambas demos son ESM plano.

## Ejecutar

```bash
node offset-cursor.mjs   # 5 páginas de 20 sobre 95 usuarios, cursores tipo b2Zmc2V0OjE5
node keyset-cursor.mjs   # mismo recorrido, los cursores llevan created_at + id
```

## En qué fijarse

- Ambos resolvers piden `limit + 1` filas, se quedan con `limit` y usan la fila
  extra para fijar `hasNextPage`: la forma estándar de evitar una segunda
  consulta.
- `mock-db.mjs` cuenta consultas: la demo de offset hace un `COUNT(*)` más una
  consulta de página por petición; la de keyset solo necesita la de página.
- Los cursores son strings base64 opacos. Las demos los decodifican como lo
  haría un resolver real, pero nada en la salida del cliente depende del
  formato.
- `hasPreviousPage` es `offset > 0` en la versión de offset y `after != null`
  en la de keyset: una simplificación que funciona para feeds que solo avanzan.

## Extensiones habituales

- Acota `first` con un `MAX_PAGE_SIZE` para que ningún cliente descargue la
  tabla entera.
- La paginación hacia atrás (`last`/`before`) es el espejo de la hacia
  adelante: lee la página en orden inverso y dale la vuelta.
- Para campos muchos-a-muchos (usuario → publicaciones → etiquetas), pagina a
  través de la tabla de enlace manteniendo la misma forma de connection.
