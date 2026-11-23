from page_controller import (
    CONTROLLERS,
    Request,
    handle_request,
)


def test_home_page_returns_200():
    resp = handle_request(Request("/", {}))
    assert resp.status == 200
    assert "Home Page" in resp.body


def test_user_profile_uses_param():
    resp = handle_request(Request("/user", {"id": "42"}))
    assert "User ID: 42" in resp.body


def test_user_profile_defaults_to_guest():
    resp = handle_request(Request("/user", {}))
    assert "guest" in resp.body


def test_order_history_lists_orders():
    resp = handle_request(Request("/orders", {"user_id": "7"}))
    assert "Order 1" in resp.body and "99.99" in resp.body


def test_unknown_path_returns_404():
    resp = handle_request(Request("/missing", {}))
    assert resp.status == 404


def test_route_map_stays_declarative():
    # adding a page = new controller + one map entry, nothing else
    assert set(CONTROLLERS) == {"/", "/user", "/orders"}
