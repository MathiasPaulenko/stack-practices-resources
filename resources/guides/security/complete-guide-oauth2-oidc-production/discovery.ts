// auth/discovery.ts — Fetch OIDC endpoints from the discovery document
export interface OidcConfig {
  issuer: string;
  authorization_endpoint: string;
  token_endpoint: string;
  userinfo_endpoint: string;
  jwks_uri: string;
  end_session_endpoint?: string;
  revocation_endpoint?: string;
  introspection_endpoint?: string;
  pushed_authorization_request_endpoint?: string;
  scopes_supported?: string[];
  response_types_supported?: string[];
  grant_types_supported?: string[];
  token_endpoint_auth_methods_supported?: string[];
}

export async function getOidcConfig(issuer: string): Promise<OidcConfig> {
  const response = await fetch(`${issuer}/.well-known/openid-configuration`);
  if (!response.ok) throw new Error(`Discovery failed for ${issuer}`);
  return response.json() as Promise<OidcConfig>;
}
