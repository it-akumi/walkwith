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


def test_post_spot_with_required_params(client):
    params = json.dumps({"name": "test spot", "latitude": 35.658581, "longitude": 139.745433, "guide": "Possible to create new spot with required params."})
    response = client.simulate_post('/spots', body=params)
    assert response.headers['location'] == '/spots/1'
    assert response.status == falcon.HTTP_CREATED


def test_post_spot_with_missing_params(client):
    params = json.dumps({"name": "test spot", "latitude": 35.658581, "guide": "Unable to create new spot because of missing longitude."})
    response = client.simulate_post('/spots', body=params)
    assert response.status == falcon.HTTP_BAD_REQUEST


def test_get_non_existing_spot(client):
    response = client.simulate_get('/spots/0')
    assert response.status == falcon.HTTP_NOT_FOUND


def test_get_existing_spot(client):
    response = client.simulate_get('/spots/1')
    spot = b'{"name": "test spot", "latitude": 35.658581, "longitude": 139.745433, "guide": "Possible to create new spot with required params."}'
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert response.content == spot
    assert response.status == falcon.HTTP_OK


def test_delete_existing_spot(client):
    response = client.simulate_delete('/spots/1')
    assert response.status == falcon.HTTP_NO_CONTENT


def test_delete_non_existing_spot(client):
    response = client.simulate_delete('/spots/0')
    assert response.status == falcon.HTTP_NOT_FOUND
