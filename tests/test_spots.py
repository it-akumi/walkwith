# coding:utf-8
"""Tests for Spot resources."""
import json
import os

import falcon


# This test must be executed before test_delete_existing_spot
def test_get_all_spots(client):
    all_spots = {
        'spots': [
            {
                "name": "test spot for GET",
                "latitude": 35.658581,
                "longitude": 139.745433,
                "guide": "Spot for test_get_existing_spot."
            },
            {
                "name": "test spot for DELETE",
                "latitude": 46.769692,
                "longitude": 150.856544,
                "guide": "Spot for test_delete_existing_spot."
            }
        ]
    }
    response = client.simulate_get('/spots')
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert json.loads(response.content) == all_spots
    assert response.status == falcon.HTTP_OK


def test_post_spot_with_required_params(client):
    """Enable to create new spot with required params."""
    params = json.dumps({
        "name": "test spot",
        "latitude": 35.658581,
        "longitude": 139.745433,
        "guide": "This is a test."
    })
    response = client.simulate_post(
        '/spots',
        body=params,
        headers={'content-type': 'application/json'}
    )
    assert response.headers['location'] == '/spots/3'
    assert response.status == falcon.HTTP_CREATED


def test_post_spot_with_missing_params(client):
    """Unable to create new spot because of missing longitude."""
    params = json.dumps({
        "name": "test spot",
        "latitude": 35.658581,
        "guide": "This is a test."
    })
    response = client.simulate_post(
        '/spots',
        body=params,
        headers={'content-type': 'application/json'}
    )
    assert response.status == falcon.HTTP_BAD_REQUEST


def test_post_spot_with_too_long_params(client):
    """Unable to create new spot because name is too long."""
    params = json.dumps({
        "name": "This name is too long",
        "latitude": 35.658581,
        "longitude": 139.745433,
        "guide": "This is a test."
    })
    response = client.simulate_post(
        '/spots',
        body=params,
        headers={'content-type': 'application/json'}
    )
    assert response.status == falcon.HTTP_BAD_REQUEST


def test_post_spot_with_invalid_type_params(client):
    """Unable to create new spot because name is not string."""
    params = json.dumps({
        "name": 0.0,
        "latitude": 35.658581,
        "longitude": 139.745433,
        "guide": "This is a test."
    })
    response = client.simulate_post(
        '/spots',
        body=params,
        headers={'content-type': 'application/json'}
    )
    assert response.status == falcon.HTTP_BAD_REQUEST


def test_post_spot_with_undefined_params(client):
    """Unable to create new spot because of undefined params."""
    params = json.dumps({
        "name": "test spot",
        "latitude": 35.658581,
        "longitude": 139.745433,
        "guide": "This is a test.",
        "hoge": "fuga"
    })
    response = client.simulate_post(
        '/spots',
        body=params,
        headers={'content-type': 'application/json'}
    )
    assert response.status == falcon.HTTP_BAD_REQUEST


def test_post_spot_without_json_params(client):
    """Unable to create new spot because parameter isn't json."""
    params = '<h1>This is a test.</h1>'
    response = client.simulate_post(
        '/spots',
        body=params,
        headers={'content-type': 'text/html'}
    )
    assert response.status == falcon.HTTP_UNSUPPORTED_MEDIA_TYPE


def test_get_non_existing_spot(client):
    response = client.simulate_get('/spots/0')
    assert response.status == falcon.HTTP_NOT_FOUND


def test_get_existing_spot(client):
    response = client.simulate_get('/spots/1')
    spot = {
        "name": "test spot for GET",
        "latitude": 35.658581,
        "longitude": 139.745433,
        "guide": "Spot for test_get_existing_spot."
    }
    assert response.headers['content-type'] == falcon.MEDIA_JSON
    assert json.loads(response.content) == spot
    assert response.status == falcon.HTTP_OK


def test_delete_spot_without_auth(client):
    response = client.simulate_delete('/spots/2')
    assert response.status == falcon.HTTP_UNAUTHORIZED
    # Really means "unauthenticated"


def test_delete_spot_with_invalid_token(client):
    response = client.simulate_delete(
        '/spots/2',
        headers={'Authorization': 'invalid_token'}
    )
    assert response.status == falcon.HTTP_FORBIDDEN
    # Really means "unauthorized"


def test_delete_existing_spot(client):
    response = client.simulate_delete(
        '/spots/2',
        headers={'Authorization': os.getenv('AUTH_TOKEN')}
    )
    assert response.status == falcon.HTTP_NO_CONTENT


def test_delete_non_existing_spot(client):
    response = client.simulate_delete(
        '/spots/0',
        headers={'Authorization': os.getenv('AUTH_TOKEN')}
    )
    assert response.status == falcon.HTTP_NOT_FOUND
