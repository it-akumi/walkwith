# coding:utf-8
import os
from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, Integer,
                        Unicode, create_engine)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def init_db():
    """Create engine and table."""
    database_tpl = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    if os.getenv('HEROKU'):
        from urllib import parse
        parse.uses_netloc.append('postgres')
        url = parse.urlparse(os.environ['DATABASE_URL'])
        database = database_tpl.format(
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            dbname=url.path[1:]
        )
    else:
        database = database_tpl.format(
            user=os.getenv('PG_USER', ''),
            password=os.getenv('PG_PASSWORD', ''),
            host=os.getenv('PG_HOST', ''),
            port=os.getenv('PG_PORT', ''),
            dbname=os.getenv('PG_DBNAME', '')
        )

    engine = create_engine(database)
    Base.metadata.create_all(bind=engine)

    return engine


class Spots(Base):
    """Definition of table of spots."""

    __tablename__ = 'spots'
    spot_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    name = Column(Unicode(20), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    guide = Column(Unicode(100))
