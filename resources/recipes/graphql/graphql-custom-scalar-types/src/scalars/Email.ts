import { GraphQLScalarType, Kind } from 'graphql';

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const EmailScalar = new GraphQLScalarType({
  name: 'Email',
  description: 'Email address string',

  serialize(value: unknown): string {
    if (typeof value !== 'string' || !EMAIL_REGEX.test(value)) {
      throw new Error(`Invalid email: ${value}`);
    }
    return value;
  },

  parseValue(value: unknown): string {
    if (typeof value !== 'string' || !EMAIL_REGEX.test(value)) {
      throw new Error(`Invalid email: ${value}`);
    }
    return value.toLowerCase();
  },

  parseLiteral(ast): string {
    if (ast.kind !== Kind.STRING || !EMAIL_REGEX.test(ast.value)) {
      throw new Error('Invalid email literal');
    }
    return ast.value.toLowerCase();
  },
});
