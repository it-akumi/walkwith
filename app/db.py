# coding:utf-8
from sqlalchemy import Column, DateTime, Float, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Spots(Base):
    __tablename__ = 'spots'
    spot_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    name = Column(Unicode(20))
    latitude = Column(Float)
    longitude = Column(Float)
    guide = Column(Unicode(100))
