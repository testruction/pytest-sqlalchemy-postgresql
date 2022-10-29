# -*- coding: utf-8 -*-

import sqlalchemy as db
from sqlalchemy.orm import Session

from app.config import ProductionConfig

engine = db.create_engine(ProductionConfig.SQLALCHEMY_DATABASE_URI)
engine.connect()
session = Session(bind=engine)
