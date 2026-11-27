from shop.modules.catalog.api.catalog_api import CatalogApi


def test_catalog_api_creates_product():
    api = CatalogApi()
    product = api.create_product("SKU-1", "Keyboard", 4990)
    assert product.sku == "SKU-1"
    assert product.price.amount_cents == 4990
    assert product.active
