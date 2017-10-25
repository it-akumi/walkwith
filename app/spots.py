# coding:utf-8
import json

import falcon


class Spot():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_CREATED
