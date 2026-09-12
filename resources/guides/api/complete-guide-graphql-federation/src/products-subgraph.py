from ariadne import QueryType, make_federated_schema, ObjectType
from ariadne.asgi import GraphQL
import httpx

type_defs = """
    type Product @key(fields: "id") {
        id: ID!
        name: String!
        price: Float!
        description: String
    }

    type Query {
        product(id: ID!): Product
        products: [Product!]!
    }
"""

query = QueryType()
product_obj = ObjectType("Product")

@query.field("product")
async def resolve_product(_, info, id):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://products-service/products/{id}")
        return resp.json()

@query.field("products")
async def resolve_products(_, info):
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://products-service/products")
        return resp.json()

@product_obj.field("__resolve_reference")
async def resolve_product_reference(reference, info):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://products-service/products/{reference['id']}")
        return resp.json()

schema = make_federated_schema(type_defs, [query, product_obj])
app = GraphQL(schema, debug=True)
