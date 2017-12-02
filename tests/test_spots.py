# coding:utf-8
import falcon
from falcon import testing
import pytest

from app.main import create_api


@pytest.fixture
def client():
    return testing.TestClient(create_api())


def test_get_all_spots(client):
    response = client.simulate_get('/spots')
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert response.status == falcon.HTTP_OK


def test_get_existing_spot(client):
    response = client.simulate_get('/spots/1')
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert response.status == falcon.HTTP_OK


def test_get_non_existing_spot(client):
    response = client.simulate_get('/spots/0')
    assert response.status == falcon.HTTP_NOT_FOUND


def test_post_spot(client):
    response = client.simulate_post('/spots')
    assert response.status == falcon.HTTP_CREATED
