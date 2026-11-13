import { GraphQLScalarType, Kind, type ValueNode } from 'graphql';

export const JSONScalar = new GraphQLScalarType({
  name: 'JSON',
  description: 'Arbitrary JSON value',

  serialize(value: unknown): unknown {
    return value;
  },

  parseValue(value: unknown): unknown {
    return value;
  },

  parseLiteral(ast): unknown {
    switch (ast.kind) {
      case Kind.STRING:
        return ast.value;
      case Kind.INT:
        return parseInt(ast.value, 10);
      case Kind.FLOAT:
        return parseFloat(ast.value);
      case Kind.BOOLEAN:
        return ast.value;
      case Kind.LIST:
        return ast.values.map((v) => parseLiteralRecursive(v));
      case Kind.OBJECT:
        return Object.fromEntries(
          ast.fields.map((field) => [field.name.value, parseLiteralRecursive(field.value)])
        );
      case Kind.NULL:
        return null;
      default:
        throw new Error(`Unexpected AST kind: ${ast.kind}`);
    }
  },
});

function parseLiteralRecursive(ast: ValueNode): unknown {
  return JSONScalar.parseLiteral!(ast, {});
}
