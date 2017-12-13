# coding:utf-8
"""Test for Root resouce."""
import falcon


def test_get_root(client):
    """Check if 'GET /' is redirected to 'GET /index.html'"""
    response = client.simulate_get('/')
    assert response.headers['location'] == '/index.html'
    assert response.status == falcon.HTTP_MOVED_PERMANENTLY
