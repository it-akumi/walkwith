# coding:utf-8
import falcon

from app.root import Root
from app.spots import Spot


def create_api():
    api = falcon.API()

    root = Root()
    spots = Spot()
    api.add_route('/', root)
    api.add_route('/spots', spots)

    return api


def main():
    return create_api()
