import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { defaultFieldResolver, GraphQLSchema } from 'graphql';
import type { DocumentNode } from 'graphql';
import type { IResolvers } from '@graphql-tools/utils';

// Builds the executable schema and wraps every field marked @auth so
// it throws Unauthorized when the context has no user.
export const authDirective = (typeDefs: DocumentNode, resolvers: IResolvers): GraphQLSchema => {
  const schema = makeExecutableSchema({ typeDefs, resolvers });

  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const usesAuth = getDirective(schema, fieldConfig, 'auth')?.[0];
      if (!usesAuth) return fieldConfig;

      const { resolve = defaultFieldResolver } = fieldConfig;
      fieldConfig.resolve = (source, args, context, info) => {
        if (!context.user) throw new Error('Unauthorized');
        return resolve(source, args, context, info);
      };
      return fieldConfig;
    },
  });
};
