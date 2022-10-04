import uuid

from responses import empty_success_response, not_found_response
from models import DailyReturn
from sqlalchemy.orm import Session
from schemas import DailyReturnEntry
from pydantic import UUID4
from typing import Dict
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def get_latest_price(db: Session, portfolio_id: UUID4) -> Dict:
    """
    :param db: Session
    :param portfolio_id: UUID4
    :return: Dictionary with fetched daily return or no entry found
    """
    fetched_entry = db.query(DailyReturn).filter(DailyReturn.portfolio_id == portfolio_id).first()
    response = empty_success_response
    if not fetched_entry:
        response['status_code'] = 404
        response['error'] = 'No entry found with given ID'
        response['requested_id'] = portfolio_id
    else:
        response['status_code'] = 200
        response['data'] = {
            fetched_entry
        }
    return response  # pragma: nocover


def create_latest_price_entry(db: Session, portfolio_id: UUID4, amount: float) -> Dict:
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
        response = empty_success_response
        response['data'] = new_user_entry
    except IntegrityError as e:
        response = not_found_response
        response['error'] = e
        return response
    return response  # pragma: nocover


def delete_entry(db: Session, entry_id: UUID4) -> Dict:
    queried_entry = db.query(DailyReturn).filter(DailyReturn.portfolio_id == entry_id).first()
    if queried_entry:
        try:
            db.delete(queried_entry)
            db.commit()
            response = empty_success_response
            response['status_code'] = 200
            response['data'] = {
                'message': 'Entry deleted',
                'delete_id': entry_id
            }
            return response
        except IntegrityError as e:
            response = not_found_response
            response['error'] = e
            return response
    else:
        response = not_found_response
        response['data'] = {
            'message': 'ID NOT FOUND',
            'searched_id': entry_id
        }
        return response
# def update_price_entry(db: Session, amount: float, user_portfolio_id: str) -> Dict:
