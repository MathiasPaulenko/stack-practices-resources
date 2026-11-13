import { RemoteGraphQLDataSource } from '@apollo/gateway';

// Forwards only what subgraphs need. The raw Authorization header
// stays at the gateway; subgraphs receive a resolved user identity.
export class AuthenticatedDataSource extends RemoteGraphQLDataSource {
  willSendRequest({ request, context }) {
    request.http.headers.set('x-user-id', context.user?.id ?? '');
    request.http.headers.set('x-user-roles', (context.user?.roles ?? []).join(','));
    request.http.headers.set('x-correlation-id', context.correlationId ?? '');
  }
}
