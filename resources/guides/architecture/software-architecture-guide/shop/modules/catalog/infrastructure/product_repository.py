from shop.modules.catalog.domain.product import Product


class ProductRepository:
    """Django-ORM-backed repository stub. The only place the catalog module
    touches persistence — domain and application layers never see the ORM."""

    def find_by_sku(self, sku: str) -> Product | None:
        return None  # ProductModel.objects.filter(sku=sku).first() -> to_domain()

    def save(self, product: Product) -> Product:
        return product  # upsert ProductModel, return refreshed domain object
