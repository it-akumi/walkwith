# coding:utf-8
import json
import os

import falcon
from falcon import testing
import pytest

from app.db import Base
from app.db import DB
from app.main import create_api


@pytest.fixture(scope='session')
def db():
    os.environ['PG_USER'] = os.getenv('PG_TEST_USER', '')
    os.environ['PG_PASSWORD'] = os.getenv('PG_TEST_PASSWORD', '')
    os.environ['PG_HOST'] = os.getenv('PG_TEST_HOST', '')
    os.environ['PG_PORT'] = os.getenv('PG_TEST_PORT', '')
    os.environ['PG_DBNAME'] = os.getenv('PG_TEST_DBNAME', '')

    db = DB()
    return db


@pytest.fixture(scope='session')
def db_table(request, db):
    Base.metadata.create_all(bind=db.engine)

    def teardown():
        Base.metadata.drop_all(bind=db.engine)

    # request.addfinalizer(teardown)


@pytest.fixture
def client():
    return testing.TestClient(create_api())


pytestmark = pytest.mark.usefixtures('db_table')


def test_get_all_spots(client):
    all_spots = {'spots': []}
    response = client.simulate_get('/spots')
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert json.loads(response.content) == all_spots
    assert response.status == falcon.HTTP_OK


def test_post_spot(client):
    params = b'''{
        "name": "test spot",
        "latitude": 35.658581,
        "longitude": 139.745433,
        "guide": "Try to create new spot."
    }'''
    response = client.simulate_post('/spots', body=params)
    assert response.headers['location'] == '/spots/1'
    assert response.status == falcon.HTTP_CREATED


def test_get_non_existing_spot(client):
    response = client.simulate_get('/spots/0')
    assert response.status == falcon.HTTP_NOT_FOUND


def test_get_existing_spot(client):
    response = client.simulate_get('/spots/1')
    spot = b'{"name": "test spot", "latitude": 35.658581, "longitude": 139.745433, "guide": "Try to create new spot."}'
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert response.content == spot
    assert response.status == falcon.HTTP_OK
