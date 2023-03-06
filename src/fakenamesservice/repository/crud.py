import traceback
import logging

from sqlalchemy.orm import Session

from fakenamesservice.repository import models, schemas

from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


def create(db: Session, identity: schemas.FakenamesCreate) -> bool:
    """ Creates a database entry """
    response = None

    with tracer.start_as_current_span(name='create'):
        current_span = trace.get_current_span()
        # current_span.set_attributes({'enduser.id': get_openid_user()})

        try:
            db_identity = models.Fakenames(**identity)
            guid = db_identity.guid
            db.add(db_identity)
            db.commit()

            logger.info(f'Creating row "{guid}" succeeded!')
            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Creating row failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = False

        current_span.set_status(status)
    return False if response is False else True


def read_all(db: Session, skip: int = 0, limit: int = 100):
    """ Retreive all records from the table """
    response = None

    with tracer.start_as_current_span(name='read_all'):
        current_span = trace.get_current_span()
        # current_span.set_attributes({'enduser.id': get_openid_user()})
        try:
            response = db.query(models.Fakenames).offset(skip).limit(limit).all()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Reading rows failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)

        current_span.set_status(status)
    return response


def read(db: Session, guid: str):
    """ Retrieves a given identity by its GUID """
    response = None

    with tracer.start_as_current_span(name='read'):
        current_span = trace.get_current_span()
        # current_span.set_attributes({'enduser.id': get_openid_user()})
        current_span.set_attributes({'fakenames.guid': guid})
        try:
            response = db.query(models.Fakenames).filter(models.Fakenames.guid == guid).first()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Reading row "{guid}" failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)

        current_span.set_status(status)
    return response


def update(db: Session, identity: schemas.FakenamesCreate) -> bool:
    """ Update a givent identity """
    response = None
    guid = None

    with tracer.start_as_current_span(name='update'):
        current_span = trace.get_current_span()
        # current_span.set_attributes({'enduser.id': get_openid_user()})
        try:
            db_identity = models.Fakenames(**identity)
            guid = db_identity.guid
            db.merge(db_identity)
            db.commit()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Updating row "{guid}" failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = False

        current_span.set_status(status)
    return False if response is False else True


def delete(db: Session, guid: str) -> bool:
    """ Deletes a given identity by its GUID """
    response = None

    with tracer.start_as_current_span(name='delete'):
        current_span = trace.get_current_span()
        # current_span.set_attributes({'enduser.id': get_openid_user()})
        try:
            db.query(models.Fakenames).filter(models.Fakenames.guid == guid).delete()
            db.commit()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Creating row "{guid}" failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = False

        current_span.set_status(status)
    return False if response is False else True
