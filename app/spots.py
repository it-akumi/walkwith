# coding:utf-8
import json

import falcon
from falcon.media.validators import jsonschema

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

    schema = {
        "properties": {
            "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
            },
            "latitude": {
                "type": "number"
            },
            "longitude": {
                "type": "number"
            },
            "guide": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100
            }
        },
        "required": [
            "name",
            "latitude",
            "longitude"
        ],
        "additionalProperties": False
    }

    @jsonschema.validate(schema)
    def on_post(self, req, resp):
        """Create new spot and return its location."""
        if req.get_header('content-type') != 'application/json':
            raise falcon.HTTPUnsupportedMediaType

        new_spot = Spots(**req.media)
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
