import pytest
import responses


@pytest.fixture
def mock_api():
    with responses.RequestsMock() as rsps:
        yield rsps
