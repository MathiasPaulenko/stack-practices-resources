// auth-directive.js — @auth(requires: Role!) with graphql-tools v8+ API
// mapSchema + getDirective replaced SchemaDirectiveVisitor (removed in
// @graphql-tools v8, 2021).
import { mapSchema, getDirective, MapperKind } from "@graphql-tools/utils";
import { defaultFieldResolver, GraphQLError } from "graphql";

const roleHierarchy = { GUEST: 0, USER: 1, ADMIN: 2 };

function hasRole(userRole, requiredRole) {
  return (roleHierarchy[userRole] ?? -1) >= (roleHierarchy[requiredRole] ?? 999);
}

export function authDirectiveTransformer(schema) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, "auth")?.[0];
      if (!authDirective) return fieldConfig;

      const requiredRole = authDirective.requires;
      const { resolve = defaultFieldResolver } = fieldConfig;

      fieldConfig.resolve = async (source, args, ctx, info) => {
        if (!ctx.user) {
          throw new GraphQLError("Not authenticated", {
            extensions: { code: "UNAUTHENTICATED" },
          });
        }
        if (!hasRole(ctx.user.role, requiredRole)) {
          throw new GraphQLError(`Requires ${requiredRole} role`, {
            extensions: { code: "FORBIDDEN" },
          });
        }
        return resolve(source, args, ctx, info);
      };
      return fieldConfig;
    },
  });
}
