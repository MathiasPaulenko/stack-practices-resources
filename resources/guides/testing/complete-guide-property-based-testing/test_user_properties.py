# Composite strategies and roundtrip properties.
# Run: pytest test_user_properties.py -v
import json
from hypothesis import given, strategies as st, composite, example

@composite
def valid_email(draw):
    """Generate valid email addresses (categories= replaces removed whitelist_categories)."""
    local = draw(st.text(min_size=1, max_size=20,
                         alphabet=st.characters(categories=("Ll", "Nd"))))
    domain = draw(st.text(min_size=1, max_size=10,
                          alphabet=st.characters(categories=("Ll", "Nd"))))
    tld = draw(st.sampled_from(["com", "org", "net", "io", "dev"]))
    return f"{local}@{domain}.{tld}"

@composite
def user_strategy(draw):
    """Generate user objects with valid fields."""
    return {
        "id": draw(st.integers(min_value=1, max_value=1000000)),
        "name": draw(st.text(min_size=1, max_size=50)),
        "email": draw(valid_email()),
        "age": draw(st.integers(min_value=0, max_value=150)),
        "is_active": draw(st.booleans()),
    }

@given(user_strategy())
@example({"id": 1, "name": "a", "email": "a@b.com", "age": 0, "is_active": False})
def test_user_serialization_roundtrip(user):
    """Serializing and deserializing a user preserves all fields."""
    assert json.loads(json.dumps(user)) == user

@given(user_strategy())
def test_user_email_contains_at(user):
    """Every generated user email contains @."""
    assert "@" in user["email"]
