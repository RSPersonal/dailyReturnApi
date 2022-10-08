import databases
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DEBUG = os.getenv("DEBUG", config("DEBUG"))

DATABASE_URL = os.getenv("DATABASE_URL_PROD", config("DATABASE_URL_PROD"))
if DEBUG:
    DATABASE_URL = os.getenv("DATABASE_URL_LOCAL", config("DATABASE_URL_LOCAL"))

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
