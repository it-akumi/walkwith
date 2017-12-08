# coding:utf-8
"""Tests for Spot resources."""
import json

import falcon


def test_get_all_spots(client):
    all_spots = {'spots': []}
    response = client.simulate_get('/spots')
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert json.loads(response.content) == all_spots
    assert response.status == falcon.HTTP_OK


def test_post_spot(client):
    params = json.dumps({"name": "test spot", "latitude": 35.658581, "longitude": 139.745433, "guide": "Try to create new spot."})
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
