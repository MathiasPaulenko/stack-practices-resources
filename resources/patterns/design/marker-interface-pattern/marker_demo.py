# Marker Interface Pattern — Python demo
# Python has no interfaces; an empty ABC base class acts as the marker.
# (An empty @runtime_checkable Protocol would NOT work: structural subtyping
# matches every object when the protocol has zero members.)

from abc import ABC
import pickle


# Marker base classes: empty but real — subclasses opt in explicitly
class Serializable(ABC):
    """Marker: subclasses declare they can be pickled."""
    pass


class Cloneable(ABC):
    """Marker: subclasses declare they support deepcopy."""
    pass


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User({self.name!r}, {self.email!r})"


class SecretData:
    def __init__(self, data: str):
        self.data = data


# Explicit opt-in through the markers
class SerializableUser(User, Serializable, Cloneable):
    pass


class Serializer:
    """Framework component that uses marker checks."""

    @staticmethod
    def safe_serialize(obj) -> bytes:
        if not isinstance(obj, Serializable):
            raise TypeError(f"{type(obj).__name__} is not Serializable")
        return pickle.dumps(obj)


if __name__ == "__main__":
    user = SerializableUser("Alice", "alice@example.com")
    data = Serializer.safe_serialize(user)
    print(f"Serialized {len(data)} bytes")

    try:
        Serializer.safe_serialize(SecretData("top-secret"))
    except TypeError as e:
        print(f"Rejected: {e}")

    # Proof the check discriminates
    print(isinstance(user, Serializable))          # True
    print(isinstance(SecretData("x"), Serializable))  # False
