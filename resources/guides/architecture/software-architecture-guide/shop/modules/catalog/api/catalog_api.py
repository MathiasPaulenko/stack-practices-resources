from shop.modules.catalog.application.create_product import CreateProductService
from shop.modules.catalog.infrastructure.product_repository import (
    ProductRepository,
)


class CatalogApi:
    """Public interface of the catalog module. Other modules may ONLY depend
    on this class — never on domain entities or repositories. Enforced by
    import-linter contracts (see contracts/importlinter.ini)."""

    def __init__(self) -> None:
        self._create = CreateProductService(ProductRepository())

    def create_product(
        self, sku: str, name: str, price_cents: int, currency: str = "USD"
    ):
        return self._create.execute(sku, name, price_cents, currency)
