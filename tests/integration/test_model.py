# -*- coding: utf-8 -*-
import logging
for logger_name in [__name__, 'sqlalchemy.engine']:
    logger = logging.getLogger(name=logger_name)
logger.setLevel(logging.DEBUG)

import pkg_resources
dataset = pkg_resources.resource_filename(__name__, 'fakenames.csv')

from app.models import Fakenames, db, Base

def test_model_create(dbsession):
    
    import itertools
    def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    import csv
    from contextlib import closing
    
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        # logger.info(dataset)
        for row in reader:
            # logger.info(row)
            record = Fakenames(**row)
            dbsession.add(record)
        dbsession.commit()
    response = dbsession.query(Fakenames).all()

    assert len(response) == 1000
    
                
def test_model_read_all(dbsession):
    response =  Fakenames.read_all()
    logger.info(len(response))
    assert len(response) == 1000

# def test_model_read(flask_app):
#     flask_app.app_context().push()
    
#     response = Fakenames.read(guid='ee8d5509-dbce-4ae1-98c8-ba8e00ca8180')
#     logger.info(response)
#     assert response