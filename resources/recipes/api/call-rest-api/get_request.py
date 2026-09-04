"""GET request with requests — timeout and error handling."""
import requests


def fetch_user(user_id: int, base_url: str = "https://api.example.com") -> dict:
    """Fetch a single user by ID with timeout and status check."""
    response = requests.get(f"{base_url}/users/{user_id}", timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        user = fetch_user(1)
        print(f"User: {user.get('name', 'unknown')}")
    except requests.Timeout:
        print("Request timed out")
    except requests.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.ConnectionError:
        print("Connection failed")
