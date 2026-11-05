# tests/fixtures/factories.py — factory_boy test data factories.
import factory
from myapp.models import User, Order, Product

class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    status = "pending"
