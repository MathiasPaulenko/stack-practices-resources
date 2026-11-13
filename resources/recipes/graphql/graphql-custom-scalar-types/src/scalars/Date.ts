import { GraphQLScalarType, Kind } from 'graphql';

export const DateScalar = new GraphQLScalarType({
  name: 'Date',
  description: 'ISO 8601 date string',
  specifiedByURL: 'https://www.rfc-editor.org/rfc/rfc3339',

  serialize(value: unknown): string {
    if (value instanceof Date) {
      return value.toISOString();
    }
    if (typeof value === 'string') {
      const date = new Date(value);
      if (isNaN(date.getTime())) {
        throw new Error(`Invalid date string: ${value}`);
      }
      return date.toISOString();
    }
    throw new Error(`Date scalar cannot serialize ${typeof value}`);
  },

  parseValue(value: unknown): Date {
    if (typeof value !== 'string') {
      throw new Error('Date input must be a string');
    }
    const date = new Date(value);
    if (isNaN(date.getTime())) {
      throw new Error(`Invalid date string: ${value}`);
    }
    return date;
  },

  parseLiteral(ast): Date {
    if (ast.kind !== Kind.STRING) {
      throw new Error('Date input must be a string literal');
    }
    const date = new Date(ast.value);
    if (isNaN(date.getTime())) {
      throw new Error(`Invalid date string: ${ast.value}`);
    }
    return date;
  },
});
