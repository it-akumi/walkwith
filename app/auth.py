# coding:utf-8
import os
import falcon


def authorize(req, resp, _):
    """Check if request has valid authorization token."""
    token = req.get_header('Authorization')

    if token is None:
        description = 'Please provide an auth token.'
        raise falcon.HTTPUnauthorized(
            'Auth token required',
            description
        )

    if not token_is_valid(token):
        description = 'The provided auth token is not valid.'
        raise falcon.HTTPUnauthorized(
            'Authorization required',
            description
        )


def token_is_valid(token):
    """Check if authorization token is valid."""
    if token == os.getenv('AUTH_TOKEN'):
        return True
    else:
        return False
