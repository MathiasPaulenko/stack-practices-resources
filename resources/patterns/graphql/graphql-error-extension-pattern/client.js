/**
 * Client-side handling: branch on extensions.code instead of parsing message.
 * Replace the show*/redirectToLogin helpers with your UI logic.
 */
export async function fetchPost(id) {
  const response = await fetch('/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: `query { post(id: "${id}") { title body } }` }),
  });

  const { data, errors } = await response.json();

  if (errors) {
    const error = errors[0];
    const code = error.extensions?.code;

    switch (code) {
      case 'UNAUTHENTICATED':
        redirectToLogin();
        return;
      case 'NOT_FOUND':
        showNotFoundPage();
        return;
      case 'FORBIDDEN':
        showAccessDenied();
        return;
      case 'VALIDATION_ERROR':
        showFieldError(error.extensions.field, error.message);
        return;
      default:
        showGenericError(error.message);
        return;
    }
  }

  return data.post;
}
