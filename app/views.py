# coding:utf-8
import os

import falcon


class View():
    def on_get(self, req, resp, filename):
        """Return required file."""
        filepath = os.path.join('app', filename)
        try:
            with open(filepath, 'r') as f:
                resp.body = f.read()
        except FileNotFoundError:
            raise falcon.HTTPNotFound
        _, ext = os.path.splitext(filename)
        if ext == '.html':
            resp.content_type = falcon.MEDIA_HTML
