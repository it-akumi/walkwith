# coding:utf-8
import falcon


class Root():
    def on_get(self, req, resp):
        """Redirect to '/index.html'."""
        raise falcon.HTTPMovedPermanently('/index.html')
