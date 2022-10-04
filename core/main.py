import os
import uuid

import crud
from schemas import DailyReturnEntry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from database import SessionLocal, database
from sqlalchemy.orm import Session
from pydantic import UUID4
from responses import empty_success_response

API_VERSION = os.getenv("API_VERSION", config("API_VERSION"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_main():
    return {"message": "success",
            "status": 200,
            "Title": "Daily Return API",
            "Author": "Raphael Sparenberg",
            "Version": API_VERSION}


@app.get("/api/v1/daily-return/{entry_id}")
async def daily_return_item(
        entry_id: UUID4,
        db: Session = Depends(get_db)):
    """
    parameters:
    """
    response = crud.get_latest_price(db, entry_id)
    return response


@app.post("/api/v1/daily-return/new/{portfolio_id}/{amount}", response_model=DailyReturnEntry)
async def create_new_entry(portfolio_id: UUID4,
                           amount: float,
                           db: Session = Depends(get_db)):
    response = crud.create_latest_price_entry(db, portfolio_id, amount)
    return response


@app.delete("/api/v1/daily-return/delete/{portfolio_id}")
async def delete_existing_entry(portfolio_id: UUID4,
                                db: Session = Depends(get_db)):
    active_deleting = os.getenv("DELETE_ACTIVE", config("DELETE_ACTIVE"))
    if active_deleting:
        response = crud.delete_entry(db, portfolio_id)
    else:
        response = empty_success_response
        response['status_code'] = 200
        response['data'] = 'Deleting of records is deactivated'
    return response
