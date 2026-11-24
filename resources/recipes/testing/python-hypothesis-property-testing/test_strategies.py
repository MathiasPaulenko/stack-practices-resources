"""Custom Hypothesis strategies: @composite and st.builds.

Companion code for https://stackpractices.com/recipes/python-hypothesis-property-testing/

Usage:
    pytest test_strategies.py -v
"""

from dataclasses import dataclass

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import composite


@composite
def valid_email(draw):
    alphabet = st.characters(categories=("Ll", "Nd"))
    local = draw(st.text(min_size=1, max_size=20, alphabet=alphabet))
    domain = draw(st.text(min_size=1, max_size=10, alphabet=alphabet))
    tld = draw(st.sampled_from(["com", "org", "net", "io"]))
    return f"{local}@{domain}.{tld}"


@given(valid_email())
def test_email_validation(email):
    assert "@" in email
    assert "." in email.split("@")[1]


@dataclass
class User:
    id: int
    name: str
    email: str


@given(
    st.builds(
        User,
        id=st.integers(min_value=1),
        name=st.text(min_size=1),
        email=st.emails(),
    )
)
def test_user_serialization(user):
    data = {"id": user.id, "name": user.name, "email": user.email}
    reconstructed = User(**data)
    assert reconstructed == user
