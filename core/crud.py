import uuid

from responses import EMPTY_SUCCESS_RESPONSE, NOT_FOUND_RESPONSE, SERVER_ERROR_RESPONSE
from models import DailyReturn
from sqlalchemy.orm import Session
from schemas import DailyReturnEntry
from pydantic import UUID4
from typing import Dict
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder


def get_latest_price(db: Session, portfolio_id: UUID4) -> Dict:
    """
    :param db: Session
    :param portfolio_id: UUID4
    :return: Dictionary with fetched daily return or no entry found
    """
    fetched_entry = db.query(DailyReturn).filter(DailyReturn.portfolio_id == portfolio_id).first()
    if fetched_entry is None:
        response = NOT_FOUND_RESPONSE
        response['error'] = 'No entry found with given ID'
        response['requested_id'] = portfolio_id
        return response
    else:
        response = EMPTY_SUCCESS_RESPONSE
        response['data'] = {
            fetched_entry
        }
    return response  # pragma: nocover


def create_latest_price_entry(db: Session, portfolio_id: UUID4, amount: float):
    """
    :param db: Session
    :param portfolio_id: UUID4
    :param amount: float
    :return: Response
    """

    new_user_entry = DailyReturn(
        last_price=amount,
        added_on=datetime.now(),
        portfolio_id=portfolio_id
    )
    try:
        db.add(new_user_entry)
        db.commit()
        db.refresh(new_user_entry)
        response = EMPTY_SUCCESS_RESPONSE
        response['data'] = jsonable_encoder(new_user_entry)
        return response
    except IntegrityError as e:
        response = SERVER_ERROR_RESPONSE
        response['error'] = jsonable_encoder(e)
    return response  # pragma: nocover


def delete_entry(db: Session, entry_id: UUID4) -> Dict:
    queried_entry = db.query(DailyReturn).filter(DailyReturn.id == entry_id).first()
    if queried_entry:
        try:
            db.delete(queried_entry)
            db.commit()
            response = EMPTY_SUCCESS_RESPONSE
            response['status_code'] = 200
            response['data'] = {
                'detail': 'Entry deleted',
                'delete_id': entry_id
            }
            return response
        except IntegrityError as e:
            response = SERVER_ERROR_RESPONSE
            response['error'] = e
            return response
    else:
        response = NOT_FOUND_RESPONSE
        response['status_code'] = 404
        response['data'] = {
            'detail': 'ID not found',
            'searched_id': entry_id
        }
        return response


def update_price_entry(entry_id: UUID4, db: Session, amount: float) -> Dict:
    queried_entry = db.query(DailyReturn).filter(DailyReturn.portfolio_id == entry_id).first()
    response = NOT_FOUND_RESPONSE
    if queried_entry is None:
        NOT_FOUND_RESPONSE['data'] = {
            'detail': 'Entry not found',
            'entry_id': entry_id
        }
        return NOT_FOUND_RESPONSE
    else:
        try:
            setattr(queried_entry, 'last_price', amount)
            db.add(queried_entry)
            db.commit()
            db.refresh(queried_entry)
            response = EMPTY_SUCCESS_RESPONSE
            response['data'] = queried_entry
            return response
        except IntegrityError as e:
            response = SERVER_ERROR_RESPONSE
            response['data'] = queried_entry
            response['error'] = e
            return response
