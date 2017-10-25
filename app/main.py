# coding:utf-8
import falcon

from .spots import Spot

api = application = falcon.API()
spots = Spot()
api.add_route('/spots', spots)
