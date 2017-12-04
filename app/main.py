# coding:utf-8
import falcon

from app.db import DB
from app.root import Root
from app.spots import AllSpots
from app.spots import SingleSpot


def create_api():
    """Bind resources to URL."""
    api = falcon.API()
    db = DB()

    root = Root()
    all_spots = AllSpots(db.session)
    single_spot = SingleSpot(db.session)
    api.add_route('/', root)
    api.add_route('/spots', all_spots)
    api.add_route('/spots/{spot_id}', single_spot)

    return api


def main():
    """Run application."""
    return create_api()
