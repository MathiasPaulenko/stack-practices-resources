"""Page Controller pattern — runnable example.

Each page gets its own controller object: it reads parameters, calls
business logic, and produces the response. A flat map routes paths to
controllers — no central dispatcher.
"""

from typing import Dict


class Request:
    def __init__(self, path: str, params: Dict[str, str]):
        self.path = path
        self.params = params


class Response:
    def __init__(self, body: str, status: int = 200):
        self.body = body
        self.status = status


class HomePageController:
    def handle(self, request: Request) -> Response:
        return Response("<h1>Home Page</h1><p>Welcome!</p>")


class UserProfileController:
    def handle(self, request: Request) -> Response:
        user_id = request.params.get("id", "guest")
        return Response(f"<h1>User Profile</h1><p>User ID: {user_id}</p>")


class OrderHistoryController:
    def __init__(self, order_service):
        self.order_service = order_service

    def handle(self, request: Request) -> Response:
        user_id = request.params.get("user_id")
        orders = self.order_service.get_orders(user_id)
        html = "<h1>Order History</h1><ul>"
        for order in orders:
            html += f"<li>Order {order['id']}: ${order['total']}</li>"
        html += "</ul>"
        return Response(html)


class FakeOrderService:
    def get_orders(self, user_id):
        return [{"id": 1, "total": 99.99}, {"id": 2, "total": 12.50}]


CONTROLLERS = {
    "/": HomePageController(),
    "/user": UserProfileController(),
    "/orders": OrderHistoryController(FakeOrderService()),
}


def handle_request(request: Request) -> Response:
    controller = CONTROLLERS.get(request.path)
    if controller:
        return controller.handle(request)
    return Response("Not Found", 404)


if __name__ == "__main__":
    resp = handle_request(Request("/user", {"id": "42"}))
    print(resp.status, resp.body)
