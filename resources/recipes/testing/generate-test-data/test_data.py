"""Deterministic test data generators: Faker + factory-boy + Hypothesis.

Usage:
    python test_data.py
"""

from dataclasses import dataclass
import factory
from factory import Faker as FactoryFaker
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()
Faker.seed(12345)  # Deterministic across runs


@dataclass
class User:
    id: int
    name: str
    email: str
    age: int
    is_active: bool


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = FactoryFaker("name")
    email = FactoryFaker("email")
    age = factory.Faker("random_int", min=18, max=90)
    is_active = True


class ProductProvider(BaseProvider):
    """Domain-specific provider: realistic SKU values."""

    def sku(self):
        categories = ["ELEC", "BOOK", "HOME", "TOY"]
        return f"{self.random_element(categories)}-{self.random_int(1000, 9999)}"


def main() -> None:
    # Basic field generators
    print("name:", fake.name())
    print("email:", fake.email())
    print("ipv4:", fake.ipv4())
    print("uuid4:", fake.uuid4())

    # Factory usage
    user = UserFactory()
    print("factory user:", user)
    batch = UserFactory.build_batch(5)
    print("batch size:", len(batch))
    admin = UserFactory(name="Admin User", age=30)
    print("overridden:", admin.name, admin.age)

    # Custom provider
    fake.add_provider(ProductProvider)
    print("custom sku:", fake.sku())

    # Hypothesis strategy (for property-based tests)
    import hypothesis.strategies as st

    user_strategy = st.builds(
        User,
        id=st.integers(min_value=1),
        name=st.text(min_size=1, max_size=100),
        email=st.emails(),
        age=st.integers(min_value=0, max_value=120),
        is_active=st.booleans(),
    )
    print("strategy:", user_strategy)


if __name__ == "__main__":
    main()
