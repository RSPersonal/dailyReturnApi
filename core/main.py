import os
import crud

from schemas import DailyReturnEntry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from database import SessionLocal, database
from sqlalchemy.orm import Session
from pydantic import UUID4
from responses import EMPTY_SUCCESS_RESPONSE
from fastapi.responses import JSONResponse


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
    return JSONResponse(content=
                        {"message": "success",
                         "status": 200,
                         "Title": "Daily Return API",
                         "Author": "Raphael Sparenberg",
                         "Version": API_VERSION
                         }
                        )


@app.get("/api/v1/daily-return/{entry_id}")
async def get_daily_return_item(
        entry_id: UUID4,
        db: Session = Depends(get_db)):
    """
    parameters:
    """
    response = crud.get_latest_price(db, entry_id)
    return JSONResponse(content=response)


@app.post("/api/v1/daily-return/new/{portfolio_id}/{amount}", response_model=DailyReturnEntry)
async def create_new_entry(portfolio_id: UUID4,
                           amount: float,
                           db: Session = Depends(get_db)):
    response = crud.create_latest_price_entry(db, portfolio_id, amount)
    return JSONResponse(content=response)


@app.delete("/api/v1/daily-return/delete/{entry_id}")
async def delete_existing_entry(entry_id: UUID4,
                                db: Session = Depends(get_db)):
    active_deleting = os.getenv("DELETE_ACTIVE", config("DELETE_ACTIVE"))
    if active_deleting:
        response = crud.delete_entry(db, entry_id)
    else:
        response = EMPTY_SUCCESS_RESPONSE
        response['status_code'] = 200
        response['data'] = 'Deleting of records is deactivated'
    return response


@app.patch("/api/v1/daily-return/update/{entry_id}/{update_price}")
async def update_daily_return_entry(entry_id: UUID4,
                                    update_price: float,
                                    db: Session = Depends(get_db),
                                    ):
    response = crud.update_price_entry(entry_id, db, update_price)
    return response
