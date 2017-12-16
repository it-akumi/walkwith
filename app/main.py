# coding:utf-8
import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, database
from app.root import Root
from app.spots import AllSpots, SingleSpot
from app.views import View


def create_api(session):
    """Bind resources to URL."""
    api = falcon.API()

    root = Root()
    all_spots = AllSpots(session)
    single_spot = SingleSpot(session)
    view = View()
    api.add_route('/', root)
    api.add_route('/{filename}', view)
    api.add_route('/spots', all_spots)
    api.add_route('/spots/{spot_id}', single_spot)

    return api


def main():
    """Run application."""
    engine = create_engine(database())
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    return create_api(session)
