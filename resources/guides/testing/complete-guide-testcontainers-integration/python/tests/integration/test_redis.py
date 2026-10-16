# tests/integration/test_redis.py — Redis with Testcontainers
import pytest
from testcontainers.redis import RedisContainer
import redis

@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        yield container

@pytest.fixture
def redis_client(redis_container):
    client = redis.Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        decode_responses=True,
    )
    yield client
    client.flushall()

def test_string_operations(redis_client):
    redis_client.set("key1", "value1")
    assert redis_client.get("key1") == "value1"

def test_hash_operations(redis_client):
    redis_client.hset("user:1", mapping={"name": "Alice", "email": "alice@test.com"})
    assert redis_client.hget("user:1", "name") == "Alice"
    assert redis_client.hgetall("user:1") == {"name": "Alice", "email": "alice@test.com"}

def test_list_operations(redis_client):
    redis_client.lpush("queue", "item1", "item2", "item3")
    assert redis_client.llen("queue") == 3
    assert redis_client.rpop("queue") == "item3"
