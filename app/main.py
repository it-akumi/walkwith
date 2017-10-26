# coding:utf-8
import falcon

from .root import Root
from .spots import Spot

api = application = falcon.API()
root = Root()
spots = Spot()
api.add_route('/', root)
api.add_route('/spots', spots)
