# coding:utf-8
"""Fixtures in this file will be shared among all tests."""

import os

from falcon import testing
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, Spots
from app.main import create_api


@pytest.fixture(scope='module')
def database():
    """Create database url."""
    database_tpl = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    database = database_tpl.format(
        user=os.getenv('PG_TEST_USER', ''),
        password=os.getenv('PG_TEST_PASSWORD', ''),
        host=os.getenv('PG_TEST_HOST', ''),
        port=os.getenv('PG_TEST_PORT', ''),
        dbname=os.getenv('PG_TEST_DBNAME', '')
    )

    return database


@pytest.fixture(scope='module')
def client(request, database):
    """Initialize DB and Create api."""
    engine = create_engine(database)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    # create spot for test_get_existing_spot
    spot = Spots(
        name="test spot for GET",
        latitude=35.658581,
        longitude=139.745433,
        guide="Spot for test_get_existing_spot."
    )
    session.add(spot)
    session.commit()

    # create spot for test_delete_existing_spot
    spot = Spots(
        name="test spot for DELETE",
        latitude=46.769692,
        longitude=150.856544,
        guide="Spot for test_delete_existing_spot."
    )
    session.add(spot)
    session.commit()

    def teardown():
        session.close()
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)

    return testing.TestClient(create_api(session))
