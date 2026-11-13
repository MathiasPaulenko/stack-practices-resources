import { GraphQLScalarType, Kind } from 'graphql';

function toURL(value: unknown): URL {
  if (typeof value !== 'string') {
    throw new Error('URL input must be a string');
  }
  const url = new URL(value); // throws TypeError on malformed input
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error(`URL must use http or https, got: ${url.protocol}`);
  }
  return url;
}

export const URLScalar = new GraphQLScalarType({
  name: 'URL',
  description: 'Absolute HTTP(S) URL',

  serialize(value: unknown): string {
    return toURL(value).toString();
  },

  parseValue(value: unknown): string {
    return toURL(value).toString();
  },

  parseLiteral(ast): string {
    if (ast.kind !== Kind.STRING) {
      throw new Error('URL input must be a string literal');
    }
    return toURL(ast.value).toString();
  },
});
