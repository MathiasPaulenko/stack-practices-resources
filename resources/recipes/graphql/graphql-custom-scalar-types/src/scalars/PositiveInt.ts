import { GraphQLScalarType, Kind } from 'graphql';

export const PositiveIntScalar = new GraphQLScalarType({
  name: 'PositiveInt',
  description: 'Integer greater than zero',

  serialize(value: unknown): number {
    if (typeof value !== 'number' || value <= 0 || !Number.isInteger(value)) {
      throw new Error(`PositiveInt cannot serialize ${value}`);
    }
    return value;
  },

  parseValue(value: unknown): number {
    if (typeof value !== 'number' || value <= 0 || !Number.isInteger(value)) {
      throw new Error(`Invalid PositiveInt: ${value}`);
    }
    return value;
  },

  parseLiteral(ast): number {
    if (ast.kind !== Kind.INT || parseInt(ast.value, 10) <= 0) {
      throw new Error('PositiveInt must be a positive integer literal');
    }
    return parseInt(ast.value, 10);
  },
});
