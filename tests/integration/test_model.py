# -*- coding: utf-8 -*-
import logging
import pkg_resources
import csv
import itertools

from contextlib import closing

from fakenamesservice.repository import crud

logger = logging.getLogger(__name__)
# for logger_name in [__name__, 'sqlalchemy.engine']:
#     logger = logging.getLogger(name=logger_name)
# logger.setLevel(logging.INFO)

dataset = pkg_resources.resource_filename(__name__,
                                          'fakenames.csv')

def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)


def test_model_create(dbsession):
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        reader = list(reader)
        
        payload = reader[25]
        logger.info(payload)
        payload['number'] = int(payload['number']) + 9000
        
        response = crud.create(dbsession, payload)
    assert response == True
        


def test_model_read_100(dbsession):
    response = crud.read_all(dbsession)
    logger.info(len(response))
    assert len(response) == 100


def test_model_read_all(dbsession):
    response = crud.read_all(dbsession, limit=1000)
    logger.info(len(response))
    assert len(response) == 1000


def test_model_read(dbsession):
    guid = '71160a30-b20f-4cef-91d9-5cf57c5112e4'
    response = crud.read(dbsession, guid=guid)
    logger.info(f'''
                number:    "{response.number}"
                firstname: "{response.givenname}"
                lastname:  "{response.surname}"
                guid:      "{response.guid}"
                ''')
    assert response.number == 50


def test_model_update(dbsession):
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        reader = list(reader)
        
        payload = reader[10]
        logger.info(payload)
        payload['number'] = int(payload['number']) + 10
        
        response = crud.update(dbsession, payload)
    assert response == True
    

def test_model_delete(dbsession):
    guid = '9dc0ed75-61fc-47a4-8ad8-57206ff37add'
    check = crud.read(dbsession, guid=guid)
    logger.info(f'''
                number:    "{check.number}"
                firstname: "{check.givenname}"
                lastname:  "{check.surname}"
                guid:      "{check.guid}"
                ''')
    response = crud.delete(dbsession, guid=guid)    
    assert response == True
