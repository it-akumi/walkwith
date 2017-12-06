# coding:utf-8
import json
import os

import falcon
from falcon import testing
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.main import create_api


def database():
    """Create database url."""
    database_tpl = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    database = database_tpl.format(
        user=os.getenv('PG_TEST_USER', ''),
        password=os.getenv('PG_TEST_PASSWORD', ''),
        host=os.getenv('PG_TEST_HOST', ''),
        port=os.getenv('PG_TEST_PORT', ''),
        dbname=os.getenv('PG_TEST_DBNAME', '')
    )

    return database


@pytest.fixture(scope='module')
def client(request):
    engine = create_engine(database())
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    def teardown():
        session.close()
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)

    return testing.TestClient(create_api(session))


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
