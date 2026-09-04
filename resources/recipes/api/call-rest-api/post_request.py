"""POST request with auth, JSON body, timeout and error handling."""
import os
import requests


def create_user(name: str, email: str, base_url: str = "https://api.example.com") -> dict:
    """Create a user via POST with Bearer auth and JSON body."""
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {"name": name, "email": email}

    response = requests.post(
        f"{base_url}/users",
        json=payload,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        created = create_user("Alice", "alice@example.com")
        print(f"Created user with ID: {created.get('id', 'unknown')}")
    except ValueError as e:
        print(f"Config error: {e}")
    except requests.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.Timeout:
        print("Request timed out")
