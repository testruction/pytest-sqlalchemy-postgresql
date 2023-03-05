from sqlalchemy import create_engine
from fakenamesservice.config import DevelopmentConfig

engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
print(engine)