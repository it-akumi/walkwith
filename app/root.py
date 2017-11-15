# coding:utf-8
import falcon


class Root():
    def on_get(self, req, resp):
        """Return top page."""
        with open('app/index.html', 'r') as f:
            resp.body = f.read()
        resp.content_type = falcon.MEDIA_HTML
        resp.status = falcon.HTTP_OK
