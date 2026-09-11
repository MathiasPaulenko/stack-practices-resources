// directives/owner.ts — Ownership-based auth directive transformer
import { defaultFieldResolver, GraphQLError } from 'graphql';
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

export function ownerDirectiveTransformer(schema: any) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig: any) => {
      const ownerDirective = getDirective(schema, fieldConfig, 'owner')?.[0];
      if (!ownerDirective) return fieldConfig;

      const { resolve = defaultFieldResolver } = fieldConfig;

      fieldConfig.resolve = async (source: any, args: any, context: any, info: any) => {
        if (!context.user) {
          throw new GraphQLError('Authentication required', {
            extensions: { code: 'FORBIDDEN' },
          });
        }

        if (source.authorId && source.authorId !== context.user.id) {
          if (context.user.role !== 'ADMIN') {
            throw new GraphQLError('You can only access your own data', {
              extensions: { code: 'FORBIDDEN' },
            });
          }
        }

        return resolve(source, args, context, info);
      };

      return fieldConfig;
    },
  });
}
