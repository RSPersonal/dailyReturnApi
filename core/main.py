import os
import sqlalchemy
import databases
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

API_VERSION = os.getenv("API_VERSION", config("API_VERSION"))
DATABASE_URL = os.getenv("DATABASE_URL", config("DATABASE_URL"))
metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/api/v1/")
async def root():
    return {"message": "success",
            "status_code": 200,
            "title": "API for getting daily return data",
            "version": API_VERSION
            }
