# coding:utf-8
import falcon
from falcon import testing
import pytest

from app.main import create_api


@pytest.fixture
def client():
    return testing.TestClient(create_api())


def test_get_root(client):
    response = client.simulate_get('/')
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert response.status == falcon.HTTP_OK
