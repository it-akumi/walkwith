# coding:utf-8
import os

from sqlalchemy import (Column, DateTime, Float, Integer,
                        Unicode, create_engine)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
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


class Spots(Base):
    __tablename__ = 'spots'

    spot_id = Column(Integer, primary_key=True,
                     autoincrement=False)
    created_at = Column(DateTime)
    name = Column(Unicode(20), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    guide = Column(Unicode(100))
