# coding:utf-8
import falcon

from app.root import Root
from app.spots import AllSpots
from app.spots import SingleSpot


def create_api():
    """Bind resources to URL."""
    api = falcon.API()

    root = Root()
    all_spots = AllSpots()
    single_spot = SingleSpot()
    api.add_route('/', root)
    api.add_route('/spots', all_spots)
    api.add_route('/spots/{spot_id}', single_spot)

    return api


def main():
    """Run application."""
    return create_api()
