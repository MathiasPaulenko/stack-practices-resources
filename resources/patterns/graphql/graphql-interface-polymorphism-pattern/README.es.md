# Patrón de Polimorfismo con Interfaces en GraphQL — Código de acompañamiento

Demo ejecutable del patrón documentado en
[stackpractices.com/es/patterns/graphql-interface-polymorphism-pattern/](https://stackpractices.com/es/patterns/graphql-interface-polymorphism-pattern/).

## Qué muestra

- Interfaces `Node` y `Searchable` implementadas por `Post`, `Comment` y `User` en SDL
- `__resolveType` basado en discriminador: los objetos traen `__typename`, la resolución es una búsqueda (nunca una adivinanza por la forma de los datos)
- Inline fragments seleccionando campos específicos sobre un tipo de retorno abstracto
- Una búsqueda `node(id)` estilo Relay que decodifica un id global base64 `Type:localId`

## Estructura

| Archivo | Propósito |
|---------|-----------|
| `schema.mjs` | typeDefs SDL + datos semilla con discriminadores `__typename` |
| `resolvers.mjs` | `__resolveType` + resolvers de campos + decodificación de `node(id)` |
| `demo.mjs` | Ejecuta una query de feed con tipos mezclados y una búsqueda por id global |
| `tests/polymorphism.test.mjs` | 6 tests sobre ejecución real de graphql-js |

## Ejecutar

```bash
npm install
npm run demo    # imprime el feed resuelto + la búsqueda node()
npm test        # 6 aserciones con vitest
```

Requiere Node 18+.
