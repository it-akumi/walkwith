# coding:utf-8
import json
import os

import falcon
from falcon import testing
import pytest

from app.main import create_api


@pytest.fixture
def client():
    return testing.TestClient(create_api())


def setup_module(module):
    os.environ['PG_USER'] = os.getenv('PG_TEST_USER', '')
    os.environ['PG_PASSWORD'] = os.getenv('PG_TEST_PASSWORD', '')
    os.environ['PG_HOST'] = os.getenv('PG_TEST_HOST', '')
    os.environ['PG_PORT'] = os.getenv('PG_TEST_PORT', '')
    os.environ['PG_DBNAME'] = os.getenv('PG_TEST_DBNAME', '')


def teardown_module(module):
    pass


def test_get_all_spots(client):
    all_spots = {'spots': []}

    response = client.simulate_get('/spots')
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert json.loads(response.content) == all_spots
    assert response.status == falcon.HTTP_OK


def test_get_non_existing_spot(client):
    response = client.simulate_get('/spots/0')
    assert response.status == falcon.HTTP_NOT_FOUND


def test_post_spot(client):
    response = client.simulate_post('/spots')
    assert response.status == falcon.HTTP_CREATED


# def test_get_existing_spot(client):
#     response = client.simulate_get('/spots/1')
#     assert response.headers['content-type'] == falcon.MEDIA_JSON
#     assert response.status == falcon.HTTP_OK
