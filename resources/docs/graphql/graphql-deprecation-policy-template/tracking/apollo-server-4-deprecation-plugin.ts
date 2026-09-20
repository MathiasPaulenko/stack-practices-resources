import type { ApolloServerPlugin } from '@apollo/server';
import type { GraphQLSchema } from 'graphql';
import { parse, visit, visitWithTypeInfo, TypeInfo } from 'graphql';

interface DeprecatedFieldHit {
  name: string;
  parentType: string;
  reason: string;
}

// Walks the query document against the schema and collects
// every selected field that carries a deprecationReason.
export function extractDeprecatedFields(
  query: string,
  schema: GraphQLSchema,
): DeprecatedFieldHit[] {
  const typeInfo = new TypeInfo(schema);
  const found: DeprecatedFieldHit[] = [];

  visit(
    parse(query),
    visitWithTypeInfo(typeInfo, {
      Field(node) {
        const fieldDef = typeInfo.getFieldDef();
        if (fieldDef?.deprecationReason) {
          found.push({
            name: `${typeInfo.getParentType()?.name}.${node.name.value}`,
            parentType: String(typeInfo.getParentType()?.name),
            reason: fieldDef.deprecationReason,
          });
        }
      },
    }),
  );
  return found;
}

// Replace with your analytics pipeline (Segment, custom events, logs, ...).
const analytics = {
  async track(event: string, properties: Record<string, unknown>) {
    console.log(event, properties);
  },
};

export const deprecationTracker: ApolloServerPlugin = {
  async requestDidStart({ request, schema }) {
    return {
      async willSendResponse({ response }) {
        const deprecated = extractDeprecatedFields(request.query ?? '', schema);
        if (deprecated.length === 0 || response.body.kind !== 'single') return;

        // Surface the warning inside the GraphQL response itself.
        response.body.singleResult.extensions = {
          ...response.body.singleResult.extensions,
          deprecations: deprecated.map((f) => ({
            field: f.name,
            reason: f.reason,
          })),
        };

        for (const field of deprecated) {
          await analytics.track('deprecated_field_used', {
            field: field.name,
            type: field.parentType,
            operationName: request.operationName ?? 'anonymous',
            client: request.http?.headers.get('x-client-id') ?? 'unknown',
            timestamp: new Date().toISOString(),
          });
        }
      },
    };
  },
};
