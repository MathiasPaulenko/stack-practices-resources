// directives/auth.ts — Role-based auth directive transformer
import { defaultFieldResolver, GraphQLError } from 'graphql';
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';
import { hasRole } from '../roleHierarchy';

export function authDirectiveTransformer(schema: any) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig: any) => {
      const authDirective = getDirective(schema, fieldConfig, 'auth')?.[0];
      if (!authDirective) return fieldConfig;

      const { requires } = authDirective;
      const { resolve = defaultFieldResolver } = fieldConfig;

      fieldConfig.resolve = async (source: any, args: any, context: any, info: any) => {
        if (!context.user) {
          throw new GraphQLError('Authentication required', {
            extensions: { code: 'FORBIDDEN' },
          });
        }

        if (requires && !hasRole(context.user.role, requires)) {
          throw new GraphQLError(`Requires role: ${requires}`, {
            extensions: { code: 'FORBIDDEN' },
          });
        }

        return resolve(source, args, context, info);
      };

      return fieldConfig;
    },
  });
}
