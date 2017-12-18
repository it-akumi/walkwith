# coding:utf-8
"""Test for View resouce."""
import falcon


def test_get_index(client):
    """Check if 'GET /index.html' returns 200."""
    response = client.simulate_get('/index.html')
    assert response.headers['content-type'] == falcon.MEDIA_HTML
    assert response.status == falcon.HTTP_OK


def test_get_non_existing_file(client):
    """Check if 'GET /not_exist.html' returns 404."""
    response = client.simulate_get('/not_exist.html')
    assert response.status == falcon.HTTP_NOT_FOUND
