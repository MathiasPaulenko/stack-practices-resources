import pytest

class TestAPISecurity:
    def test_sql_injection_in_login(self, client):
        # Test SQL injection in login
        response = client.post("/api/login", json={
            "username": "admin' OR '1'='1",
            "password": "anything"
        })
        assert response.status_code == 401
        assert "token" not in response.json()
    
    def test_mass_assignment(self, client, auth_headers):
        # Test mass assignment protection
        response = client.put("/api/users/me", json={
            "username": "newname",
            "role": "admin",  # Should be ignored
            "is_admin": True   # Should be ignored
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["role"] != "admin"
    
    def test_rate_limiting(self, client):
        # Test rate limiting
        for i in range(101):
            response = client.get("/api/data")
            if i < 100:
                assert response.status_code == 200
            else:
                assert response.status_code == 429
    
    def test_cors_headers(self, client):
        # Test CORS configuration
        response = client.options(
            "/api/data",
            headers={
                "Origin": "https://evil.com",
                "Access-Control-Request-Method": "GET"
            }
        )
        # Should not allow evil.com
        assert "access-control-allow-origin" not in response.headers or \
               response.headers["access-control-allow-origin"] != "https://evil.com"
    
    def test_authentication_required(self, client):
        # Test that protected endpoints require auth
        response = client.get("/api/users/me")
        assert response.status_code == 401
    
    def test_invalid_token_rejected(self, client):
        # Test invalid JWT
        response = client.get(
            "/api/users/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401
    
    def test_expired_token_rejected(self, client):
        # Test expired JWT
        expired_token = generate_expired_token()
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
    
    def test_pagination_limit_enforced(self, client, auth_headers):
        # Test that page size is capped
        response = client.get(
            "/api/users?size=10000",
            headers=auth_headers
        )
        data = response.json()
        assert len(data["data"]) <= 100  # MAX_PAGE_SIZE
