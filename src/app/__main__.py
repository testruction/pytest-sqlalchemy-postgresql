from sqlalchemy import create_engine
from app.config import DevelopmentConfig

engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
print(engine)