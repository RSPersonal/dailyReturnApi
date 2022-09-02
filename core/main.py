import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from database import database

API_VERSION = os.getenv("API_VERSION", config("API_VERSION"))

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
