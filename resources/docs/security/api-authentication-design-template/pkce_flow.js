// Step 1: Generate PKCE verifier and challenge
const verifier = generateRandomString(64);
const challenge = await sha256(verifier).then(base64urlEncode);
const state = generateRandomString(32);

// Step 2: Redirect to authorization endpoint
const authUrl = new URL('https://auth.example.com/authorize');
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('client_id', 'my-client-id');
authUrl.searchParams.set('redirect_uri', 'https://app.example.com/callback');
authUrl.searchParams.set('scope', 'openid profile read:orders');
authUrl.searchParams.set('state', state);
authUrl.searchParams.set('code_challenge', challenge);
authUrl.searchParams.set('code_challenge_method', 'S256');

window.location.href = authUrl.toString();

// Step 3: Exchange code for tokens (in callback)
const response = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: 'my-client-id',
        code: authCode,
        redirect_uri: 'https://app.example.com/callback',
        code_verifier: verifier,  // PKCE verifier from step 1
    }),
});

const { access_token, refresh_token, id_token, expires_in } = await response.json();
