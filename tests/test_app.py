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

def test_get_spots(client):
    response = client.simulate_get('/spots')
    assert response.status == falcon.HTTP_OK

def test_post_spots(client):
    response = client.simulate_post('/spots')
    assert response.status == falcon.HTTP_CREATED
