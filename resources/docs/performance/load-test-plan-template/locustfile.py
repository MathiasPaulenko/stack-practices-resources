import random

from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://staging.example.com"

    @task(40)
    def browse_homepage(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Homepage failed: {response.status_code}")

    @task(25)
    def view_product(self):
        product_id = random.randint(1, 10000)
        with self.client.get(f"/api/products/{product_id}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Product failed: {response.status_code}")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Product too slow")

    @task(20)
    def search(self):
        queries = ['laptop', 'phone', 'headphones', 'keyboard', 'mouse']
        query = random.choice(queries)
        with self.client.get(f"/api/search?q={query}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Search failed: {response.status_code}")

    @task(10)
    def add_to_cart(self):
        product_id = random.randint(1, 10000)
        with self.client.post("/api/cart",
            json={"product_id": product_id, "quantity": 1},
            catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Cart failed: {response.status_code}")

    @task(5)
    def checkout(self):
        with self.client.post("/api/checkout",
            json={"payment_token": "test_token", "address_id": 1},
            catch_response=True
        ) as response:
            if response.status_code not in [200, 201]:
                response.failure(f"Checkout failed: {response.status_code}")
