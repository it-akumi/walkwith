# coding:utf-8
import json

import falcon
from sqlalchemy.orm import sessionmaker

from app.db import Spots
from app.db import init_db


class Spot():
    def __init__(self):
        """Create session (interface for DB)."""
        Session = sessionmaker(bind=init_db())
        self.session = Session()

    def on_get(self, req, resp):
        """Return all spots in the form of json."""
        all_spots = self.session.query(Spots).all()
        attributes = ['name', 'latitude', 'longitude', 'guide']
        body = dict()
        body['spots'] = list(
            {attr: spot.__dict__[attr] for attr in attributes}
            for spot in all_spots
        )

        resp.body = json.dumps(body)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp):
        """Create new spot and return its location."""
        resp.status = falcon.HTTP_CREATED
