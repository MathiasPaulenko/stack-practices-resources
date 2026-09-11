// directives/permission.ts — Permission-based auth directive transformer
import { defaultFieldResolver, GraphQLError } from 'graphql';
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

export function permissionDirectiveTransformer(schema: any) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig: any) => {
      const directive = getDirective(schema, fieldConfig, 'hasPermission')?.[0];
      if (!directive) return fieldConfig;

      const { permission } = directive;
      const { resolve = defaultFieldResolver } = fieldConfig;

      fieldConfig.resolve = async (source: any, args: any, context: any, info: any) => {
        if (!context.user?.permissions?.includes(permission)) {
          throw new GraphQLError(`Missing permission: ${permission}`, {
            extensions: { code: 'FORBIDDEN' },
          });
        }
        return resolve(source, args, context, info);
      };

      return fieldConfig;
    },
  });
}
