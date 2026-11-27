from shop.modules.catalog.domain.product import Product
from shop.modules.catalog.infrastructure.product_repository import (
    ProductRepository,
)
from shop.shared.kernel.money import Money


class CreateProductService:
    """Application service: orchestrates domain objects, owns no rules itself."""

    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo

    def execute(
        self, sku: str, name: str, price_cents: int, currency: str = "USD"
    ) -> Product:
        if self._repo.find_by_sku(sku) is not None:
            raise ValueError(f"SKU {sku} already exists")
        product = Product(
            sku=sku, name=name, price=Money(price_cents, currency)
        )
        return self._repo.save(product)
