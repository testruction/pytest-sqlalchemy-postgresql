import sys
sys.path.append('.')
sys.path.append('./src/')

import logging
logger = logging.getLogger(__name__)

from sqlalchemy import create_engine 
from sqlalchemy.orm import Session
from app.config import DevelopmentConfig

import pytest


@pytest.fixture(scope="session")
def engine():
    return create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="session")
def tables(engine):
    from app.models import Base
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()