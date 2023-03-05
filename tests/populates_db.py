#!/usr/bin/env python3
import sys
sys.path.append('.')
sys.path.append('./src/')

import logging
import pkg_resources
import itertools
import csv

from contextlib import closing

from fakenamesservice.database import SessionLocal, engine
from fakenamesservice.repository import models

logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger.setLevel('DEBUG')

dataset = pkg_resources.resource_filename(__name__,
                                          'integration/fakenames.csv')

def lower_first(iterator):
    return itertools.chain([next(iterator).lower()], iterator)


with SessionLocal() as session:
    models.Base.metadata.create_all(bind=engine)

    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        for row in reader:
            data = models.Fakenames(**row)

            session.add(data)
    session.commit()
