# coding:utf-8
import falcon


class Root():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_NOT_FOUND
