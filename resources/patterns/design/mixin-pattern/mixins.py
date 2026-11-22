"""Mixin Pattern — runnable Python companion.

SerializableMixin + TimestampMixin composed into User through cooperative
multiple inheritance. Includes a unittest suite showing how to test a mixin
in isolation against a throwaway host class.

Run: python mixins.py
Tests: python -m unittest mixins -v
"""

import json
import unittest
from datetime import datetime


class SerializableMixin:
    """Adds JSON serialization to any class that stores data in __dict__."""

    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str)

    @classmethod
    def from_json(cls, data: str):
        obj = cls.__new__(cls)
        obj.__dict__.update(json.loads(data))
        return obj


class TimestampMixin:
    """Adds created_at / updated_at tracking.

    The cooperative super().__init__() call is what keeps the MRO chain
    alive — skip it and every class to the right never initializes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def touch(self):
        self.updated_at = datetime.now()


class User(TimestampMixin, SerializableMixin):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        super().__init__()


class TestSerializableMixin(unittest.TestCase):
    """The mixin is tested against a throwaway host — no domain class needed."""

    def setUp(self):
        host = type("Host", (SerializableMixin,), {})
        self.obj = host()
        self.obj.name = "x"

    def test_to_json_serializes_dict(self):
        self.assertEqual(json.loads(self.obj.to_json()), {"name": "x"})

    def test_from_json_roundtrip(self):
        clone = SerializableMixin.from_json('{"name": "y"}')
        self.assertEqual(clone.name, "y")


class TestComposedUser(unittest.TestCase):
    def test_user_gets_all_mixin_methods(self):
        user = User("Alice", "alice@example.com")
        payload = json.loads(user.to_json())
        self.assertIn("created_at", payload)
        self.assertEqual(payload["name"], "Alice")

    def test_touch_updates_timestamp(self):
        user = User("Bob", "bob@example.com")
        before = user.updated_at
        user.touch()
        self.assertGreaterEqual(user.updated_at, before)

    def test_mro_leftmost_wins(self):
        # User -> TimestampMixin -> SerializableMixin -> object
        self.assertEqual(User.__mro__[1], TimestampMixin)


if __name__ == "__main__":
    user = User("Alice", "alice@example.com")
    print(user.to_json())
    user.touch()
    unittest.main(argv=[""], exit=False, verbosity=0)
