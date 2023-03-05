import pytest
import logging
import pkg_resources
import csv

from contextlib import closing
    
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fakenamesservice.config import DevelopmentConfig
from fakenamesservice.repository import models

logger = logging.getLogger(__name__)

dataset = pkg_resources.resource_filename(__name__,
                                          'integration/fakenames.csv')

def pytest_sessionstart(session):
    engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    models.Base.metadata.create_all(engine)

    def lower_first(iterator):
        import itertools
        return itertools.chain([next(iterator).lower()], iterator)

    with Session(bind=engine) as session:
        with closing(open(dataset, encoding='utf-8-sig')) as f:
            reader = csv.DictReader(lower_first(f))

            for row in reader:
                session.add(models.Fakenames(**row))
        session.commit()
        session.close()

def pytest_unconfigure():
    engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    models.Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def engine():
    return create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, )


@pytest.fixture(scope="session")
def tables(engine):

    models.Base.metadata.create_all(engine)
    yield
    models.Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    """ Returns an sqlalchemy session, and after the test tears down everything properly."""
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
