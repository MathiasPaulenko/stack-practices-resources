"""Client that talks to the ambassador, not the external service.

Usage: point the ambassador at any HTTP endpoint. For a quick local test,
run `python -m http.server 8080` in another terminal and use
AmbassadorProxy("http://localhost:8080").
"""

from ambassador_proxy import AmbassadorProxy

ambassador = AmbassadorProxy("https://api.external.com")


def get_user_profile(user_id):
    resp = ambassador.request("GET", f"/users/{user_id}")
    return resp.json()


def create_order(order_data):
    resp = ambassador.request(
        "POST",
        "/orders",
        json=order_data,
        headers={"Content-Type": "application/json"},
    )
    return resp.json()


if __name__ == "__main__":
    stats = ambassador.get_stats()
    for endpoint, s in stats.items():
        print(
            f"{endpoint}: {s['count']} requests, {s['errors']} errors, "
            f"avg {s['avg_latency_ms']:.0f}ms"
        )
