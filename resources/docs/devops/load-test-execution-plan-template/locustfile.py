"""Locust load test matching the execution-plan template scenarios.

Run: locust -f locustfile.py --host https://api.example.com
"""

from locust import HttpUser, between, task


class CheckoutUser(HttpUser):
    """Weighted user journey: browse and search outweigh checkout, like production."""

    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "/auth/login",
            json={"username": f"user_{self.environment.parsed_options.users or 1}", "password": "test-password"},
        )
        self.token = response.json().get("token", "")

    @task(5)
    def browse_catalog(self):
        self.client.get("/products", name="S01 browse catalog")

    @task(4)
    def search(self):
        self.client.get("/search?q=shoes", name="S04 search")

    @task(3)
    def add_to_cart(self):
        self.client.post(
            "/cart/items",
            json={"product_id": 42, "quantity": 1},
            headers=self._headers(),
            name="S02 add to cart",
        )

    @task(2)
    def checkout(self):
        self.client.post(
            "/orders",
            json={"payment_method": "card", "shipping": "standard"},
            headers=self._headers(),
            name="S03 checkout",
        )

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}
