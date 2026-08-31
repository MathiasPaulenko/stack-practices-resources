from elasticsearch import Elasticsearch, BadRequestError


def seed_data(client: Elasticsearch) -> None:
    try:
        client.indices.create(
            index="products",
            mappings={
                "properties": {
                    "name": {"type": "text"},
                    "category": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}},
                    },
                    "brand": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}},
                    },
                    "price": {"type": "float"},
                    "popularity": {"type": "float"},
                }
            },
        )
    except BadRequestError:
        pass

    docs = [
        {"name": "Gaming Laptop", "category": "Laptops", "brand": "ProTech", "price": 1200.0, "popularity": 9.5},
        {"name": "Office Laptop", "category": "Laptops", "brand": "ProTech", "price": 800.0, "popularity": 7.0},
        {"name": "Ultrabook 13", "category": "Laptops", "brand": "Sleek", "price": 1500.0, "popularity": 8.5},
        {"name": "Smartphone X", "category": "Phones", "brand": "ProTech", "price": 900.0, "popularity": 9.0},
        {"name": "Budget Phone", "category": "Phones", "brand": "Sleek", "price": 250.0, "popularity": 6.5},
        {"name": "Mechanical Keyboard", "category": "Accessories", "brand": "KeyChamp", "price": 120.0, "popularity": 8.0},
        {"name": "Wireless Mouse", "category": "Accessories", "brand": "Sleek", "price": 60.0, "popularity": 7.5},
    ]

    for i, doc in enumerate(docs):
        client.index(index="products", id=i, document=doc)

    client.indices.refresh(index="products")


def category_facets(client: Elasticsearch) -> None:
    response = client.search(
        index="products",
        size=0,
        query={"match_all": {}},
        aggs={
            "categories": {
                "terms": {"field": "category.keyword", "size": 10}
            },
            "brands": {
                "terms": {"field": "brand.keyword", "size": 10}
            },
        },
    )
    print(response.body["aggregations"]["categories"]["buckets"])
    print(response.body["aggregations"]["brands"]["buckets"])


def price_stats(client: Elasticsearch) -> None:
    response = client.search(
        index="products",
        size=0,
        query={"match_all": {}},
        aggs={
            "price_stats": {"stats": {"field": "price"}},
            "price_percentiles": {
                "percentiles": {"field": "price", "percents": [25, 50, 75, 95]}
            },
        },
    )
    print(response.body["aggregations"]["price_stats"])
    print(response.body["aggregations"]["price_percentiles"])


if __name__ == "__main__":
    es = Elasticsearch("http://localhost:9200")
    seed_data(es)
    category_facets(es)
    price_stats(es)
