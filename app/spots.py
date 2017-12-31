# coding:utf-8
import json

import falcon
import sqlalchemy

from app.auth import authorize
from app.db import Spots


class Spot():
    def __init__(self, session):
        """Set db session and attributes of spot."""
        self._session = session
        # Request and response includes these attributes
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


    def validate(self, recieved_params):
        """Validate recieved parameters."""
        # If recieved undefined params
        for k in recieved_params.keys():
            if k not in self._attr:
                msg = 'You post undefined parameter.'
                raise falcon.HTTPInvalidParam(msg, k)

        # If required parameter doesn't exist
        required = ['name', 'latitude', 'longitude']
        for r in required:
            if r not in recieved_params.keys():
                raise falcon.HTTPMissingParam(r)

        # If recieved invalid params
        if len(recieved_params['name']) > 20:
            msg = 'name must be within 20 characters.'
            raise falcon.HTTPInvalidParam(msg, 'name')
        if len(recieved_params['guide']) > 100:
            msg = 'guide must be within 100 characters.'
            raise falcon.HTTPInvalidParam(msg, 'guide')


    def on_post(self, req, resp):
        """Create new spot and return its location."""
        recieved_params = json.loads(req.stream.read())
        self.validate(recieved_params)

        new_spot = Spots(**recieved_params)
        self._session.add(new_spot)
        self._session.commit()

        resp.location = '/spots/{}'.format(new_spot.spot_id)
        resp.status = falcon.HTTP_CREATED


class SingleSpot(Spot):
    def on_get(self, req, resp, spot_id):
        """Return attributes of spot in the form of json."""
        spot = self._session.query(Spots).get(spot_id)
        if spot is None:
            raise falcon.HTTPNotFound
        else:
            body = {attr: spot.__dict__[attr]
                    for attr in self._attr}
            resp.body = json.dumps(body)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK

    @falcon.before(authorize)
    def on_delete(self, req, resp, spot_id):
        """Delete requested spot."""
        spot = self._session.query(Spots).get(spot_id)
        if spot is None:
            raise falcon.HTTPNotFound
        else:
            self._session.delete(spot)
            self._session.commit()
            resp.status = falcon.HTTP_NO_CONTENT
