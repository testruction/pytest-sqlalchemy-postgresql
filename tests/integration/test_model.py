# -*- coding: utf-8 -*-
import logging

from fakenamesservice.repository import crud

logger = logging.getLogger(__name__)
# for logger_name in [__name__, 'sqlalchemy.engine']:
#     logger = logging.getLogger(name=logger_name)
# logger.setLevel(logging.INFO)

def test_model_read_100(dbsession):
    response = crud.read_all(dbsession)
    logger.info(len(response))
    assert len(response) == 100

def test_model_read_all(dbsession):
    response = crud.read_all(dbsession, limit=1000)
    logger.info(len(response))
    assert len(response) == 1000