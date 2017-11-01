# coding:utf-8
import falcon

from app.root import Root
from app.spots import Spot

api = application = falcon.API()
root = Root()
spots = Spot()
api.add_route('/', root)
api.add_route('/spots', spots)
