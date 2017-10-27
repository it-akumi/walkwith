# coding:utf-8
import falcon
from falcon import testing
import pytest

from app.main import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_get_root(client):
    response = client.simulate_get('/')
    assert response.status == falcon.HTTP_NOT_FOUND
