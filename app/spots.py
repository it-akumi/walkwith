# coding:utf-8
import json

import falcon
from sqlalchemy.orm import sessionmaker

from app.db import Spots
from app.db import init_db


class Spot():
    def __init__(self):
        """Set session and attributes of spot."""
        Session = sessionmaker(bind=init_db())
        self._session = Session()
        self._attr = ['name', 'latitude', 'longitude', 'guide']


class AllSpots(Spot):
    def on_get(self, req, resp):
        """Return attributes of all spots in the form of json."""
        all_spots = self._session.query(Spots).all()
        body = dict()
        body['spots'] = list(
            {attr: spot.__dict__[attr] for attr in self._attr}
            for spot in all_spots
        )

        resp.body = json.dumps(body)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp):
        """Create new spot and return its location."""
        sent_params = json.loads(req.stream.read())
        new_spot = Spots(**sent_params)
        self._session.add(new_spot)
        self._session.commit()

        resp.location = '/spots/{}'.format(new_spot.spot_id)
        resp.status = falcon.HTTP_CREATED


class SingleSpot(Spot):
    def on_get(self, req, resp, spot_id):
        """Return attributes of spot in the form of json."""
        spot = self._session.query(Spots).get(spot_id)
        if spot is None:
            resp.body = 'Sorry, Resource Not Found.'
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            body = {attr: spot.__dict__[attr]
                    for attr in self._attr}
            resp.body = json.dumps(body)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
