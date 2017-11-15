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
    assert response.headers['content-type'] == falcon.MEDIA_HTML
    assert response.status == falcon.HTTP_OK
