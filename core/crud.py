import json
import uuid

from fastapi.encoders import jsonable_encoder

from responses import EMPTY_SUCCESS_RESPONSE, NOT_FOUND_RESPONSE, SERVER_ERROR_RESPONSE
from models import DailyReturn
from sqlalchemy.orm import Session
from pydantic import UUID4
from typing import Dict
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from uuid import UUID


def get_latest_price(db: Session, portfolio_id: UUID4) -> str:
    """
    :param db: Session
    :param portfolio_id: UUID4
    :return: Dictionary with fetched daily return or no entry found
    """
    fetched_entry = db.query(DailyReturn) \
        .filter(DailyReturn.portfolio_id == portfolio_id) \
        .order_by(desc('added_on')) \
        .first()

    if fetched_entry is None:
        response = NOT_FOUND_RESPONSE
        response['error'] = 'No entry found with given ID'
        response['requested_id'] = str(portfolio_id)
        return response
    else:
        response = EMPTY_SUCCESS_RESPONSE
        fetched_price = fetched_entry.last_price
        response['data'] = {
            'last_price': fetched_price
        }
        response['requested_id'] = str(portfolio_id)
    return response  # pragma: nocover


def create_latest_price_entry(db: Session, portfolio_id: UUID, amount: float):
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
        new_user_entry.id = str(new_user_entry.id)
        response = EMPTY_SUCCESS_RESPONSE
        response['data'] = jsonable_encoder(new_user_entry)
        return response
    except IntegrityError as e:
        response = SERVER_ERROR_RESPONSE
        response['error'] = jsonable_encoder(e)
    return response  # pragma: nocover


def delete_entry(db: Session, entry_id: UUID4) -> Dict:
    queried_entry = db.query(DailyReturn).get(entry_id)
    if queried_entry:
        try:
            db.delete(queried_entry)
            db.commit()
            response = EMPTY_SUCCESS_RESPONSE
            response['status_code'] = 200
            response['data'] = {
                'detail': 'Entry deleted',
                'delete_id': str(entry_id)
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
            'searched_id': str(entry_id)
        }
        return response


def update_price_entry(entry_id: UUID4, db: Session, amount: float) -> Dict:
    queried_entry = db.query(DailyReturn).get(entry_id)
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
