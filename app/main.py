# coding:utf-8
import falcon

from app.db import Base, engine
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
    Base.metadata.create_all(bind=engine)
    return create_api()
