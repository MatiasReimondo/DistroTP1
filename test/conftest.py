import pytest

from api.resolver import Resolver
from app import create_app


@pytest.fixture
def app():
    _app = create_app()
    return _app


@pytest.fixture(scope="module")
def client():
    with create_app().app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def reset_resolver():
    Resolver.get_instance().domains = {}
