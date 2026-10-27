# acl_gateway.py — ACL exposed as an HTTP API
from flask import Flask, request, jsonify
from acl.customer_acl import CustomerACL
from legacy.client import LegacyCustomerClient

app = Flask(__name__)
acl = CustomerACL(LegacyCustomerClient())

@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = acl.get_customer(customer_id)
    if customer is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": customer.id,
        "email": customer.email,
        "fullName": customer.full_name,
        "status": customer.status.value
    })

@app.route("/api/customers", methods=["POST"])
def create_customer():
    data = request.json
    customer = Customer(
        id="",
        email=data["email"],
        full_name=data["fullName"],
        status=CustomerStatus.active(),
        created_at=""
    )
    created = acl.create_customer(customer)
    return jsonify({
        "id": created.id,
        "email": created.email,
        "fullName": created.full_name,
        "status": created.status.value
    }), 201
