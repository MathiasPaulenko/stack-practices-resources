# Consumer contract test with pact-python — order-service vs user-service
# Run: pytest consumer_pact_test.py
import pytest
from pact import Consumer, Provider

pact = Consumer('order-service').has_pact_with(
    Provider('user-service'),
    pact_dir='pacts/',
    host_name='localhost',
    host_port=8080,
)


@pytest.fixture
def user_client():
    return UserClient(base_url='http://localhost:8080')


def test_get_user_contract(user_client):
    (
        pact
        .given('a user with id 1 exists')
        .upon_receiving('a request for user 1')
        .with_request('GET', '/users/1', headers={'Accept': 'application/json'})
        .will_respond_with(200, body={
            'id': 1,
            'name': 'Alice',
            'email': 'alice@x.com',
            'role': 'admin',
        })
    )

    with pact:
        user = user_client.get_user(1)

    assert user['name'] == 'Alice'
    assert user['email'] == 'alice@x.com'


def test_create_user_contract(user_client):
    (
        pact
        .given('no user with email bob@x.com exists')
        .upon_receiving('a request to create a user')
        .with_request(
            'POST',
            '/users',
            headers={'Content-Type': 'application/json'},
            body={'name': 'Bob', 'email': 'bob@x.com'},
        )
        .will_respond_with(201, body={
            'id': 2,
            'name': 'Bob',
            'email': 'bob@x.com',
            'role': 'member',
        })
    )

    with pact:
        user = user_client.create_user(name='Bob', email='bob@x.com')

    assert user['id'] == 2
