# coding:utf-8
import falcon
from sqlalchemy.orm import sessionmaker

from app.db import engine


class Spot():
    def __init__(self):
        """Create session (interface for DB)."""
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def on_get(self, req, resp):
        """Return all spots in the form of json."""
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp):
        """Create new spot and return its location."""
        resp.status = falcon.HTTP_CREATED
