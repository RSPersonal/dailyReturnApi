import databases
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DATABASE_URL = os.getenv("DATABASE_URL", config("DATABASE_URL"))

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
