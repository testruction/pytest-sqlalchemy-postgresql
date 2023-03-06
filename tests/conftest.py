import pytest
import logging
import pkg_resources
import csv
import itertools

from contextlib import closing
    
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fakenamesservice.config import DevelopmentConfig
from fakenamesservice.models import models

logger = logging.getLogger(__name__)

dataset = pkg_resources.resource_filename(__name__,
                                          'integration/fakenames.csv')


@pytest.fixture(scope="session")
def engine():
    return create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, )


@pytest.fixture(scope="session")
def tables(engine):

    models.Base.metadata.create_all(engine)
    yield
    models.Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def dbsession(engine, tables):
    """ Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    Session = sessionmaker(bind=engine)

    def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    with Session.begin() as session:
        with closing(open(dataset, encoding='utf-8-sig')) as f:
            reader = csv.DictReader(lower_first(f))

            for row in reader:
                session.add(models.Fakenames(**row))
        session.commit()

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
