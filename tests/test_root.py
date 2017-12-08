# coding:utf-8
"""Test for Root resouce."""
import falcon


def test_get_root(client):
    response = client.simulate_get('/')
    assert response.headers['content-type'] == falcon.MEDIA_HTML
    assert response.status == falcon.HTTP_OK
