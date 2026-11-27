from dataclasses import dataclass

from shop.shared.kernel.base_entity import BaseEntity
from shop.shared.kernel.money import Money


@dataclass
class Product(BaseEntity):
    sku: str = ""
    name: str = ""
    price: Money = Money(0)
    active: bool = True

    def deactivate(self) -> None:
        self.active = False
