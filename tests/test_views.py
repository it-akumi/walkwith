# coding:utf-8
"""Test for View resouce."""
import falcon


def test_get_index(client):
    """Check if 'GET /index.html' returns 200."""
    response = client.simulate_get('/index.html')
    assert response.headers['content-type'] == falcon.MEDIA_HTML
    assert response.status == falcon.HTTP_OK
