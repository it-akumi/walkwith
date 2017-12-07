# coding:utf-8
import os

from falcon import testing
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.main import create_api


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
def client(request):
    engine = create_engine(database())
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    def teardown():
        session.close()
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)

    return testing.TestClient(create_api(session))
