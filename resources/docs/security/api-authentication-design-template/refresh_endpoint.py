from flask import request, response, jsonify

@app.route('/auth/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'no refresh token'}), 401

    # Validate refresh token server-side
    stored = get_refresh_token(refresh_token)
    if not stored or stored.is_expired() or stored.is_revoked():
        return jsonify({'error': 'invalid refresh token'}), 401

    # Check token rotation — old token should be invalidated
    if stored.used:
        # Possible token theft — revoke all tokens for this user
        revoke_all_tokens(stored.user_id)
        return jsonify({'error': 'token reuse detected'}), 401

    # Issue new access token
    new_access = issue_access_token(stored.user_id, stored.scopes)

    # Rotate refresh token (issue new, revoke old)
    new_refresh = issue_refresh_token(stored.user_id)
    revoke_refresh_token(refresh_token)

    resp = jsonify({'access_token': new_access})
    resp.set_cookie(
        'refresh_token',
        new_refresh,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=7 * 24 * 3600,
        path='/auth/refresh',
    )
    return resp
