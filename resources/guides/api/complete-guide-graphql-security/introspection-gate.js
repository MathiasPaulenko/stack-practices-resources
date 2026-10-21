// introspection-gate.js — allow introspection only for admin users
// Inspects the parsed operation AST (requestContext.operation), not the raw
// query string: __schema/__type are reserved field names and cannot be
// obfuscated, while substring checks fire on comments and string literals.
import { GraphQLError } from "graphql";

export const introspectionGatePlugin = {
  async requestDidStart() {
    return {
      async didResolveOperation(requestContext) {
        const selections = requestContext.operation?.selectionSet.selections ?? [];
        const isIntrospection = selections.some(
          (s) => s.kind === "Field" && (s.name.value === "__schema" || s.name.value === "__type"),
        );
        if (isIntrospection && requestContext.contextValue.user?.role !== "ADMIN") {
          throw new GraphQLError("Introspection requires admin access", {
            extensions: { code: "FORBIDDEN" },
          });
        }
      },
    };
  },
};

// Strictest posture for public APIs: accept only pre-registered operation
// hashes — raw query text is rejected outright.
export const trustedDocumentsOnly = {
  async requestDidStart() {
    return {
      async didResolveOperation(requestContext) {
        if (requestContext.request.query) {
          throw new GraphQLError("Only persisted operations are allowed", {
            extensions: { code: "FORBIDDEN" },
          });
        }
      },
    };
  },
};
