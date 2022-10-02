from models import DailyReturn
from sqlalchemy.orm import Session
from schemas import DailyReturnEntry
from pydantic import UUID4
from typing import Dict


def get_latest_price(db: Session, portfolio_id: UUID4) -> Dict:
    """
    :param db: Session
    :param portfolio_id: UUID4
    :return: Dictionary with fetched daily return or no entry found
    """
    fetched_entry = db.query(DailyReturn).filter(DailyReturn.portfolio_id == portfolio_id).first()
    response = {"message": "success",
                "status_code": None,
                "data": {}
                }
    if not fetched_entry:
        response['status_code'] = 404
        response['error'] = 'No entry found with given ID'
        response['requested_id'] = portfolio_id
    else:
        response['status_code'] = 200
        response['data'] = {
            fetched_entry
        }
    return response


def create_latest_price_entry(user_entry: DailyReturnEntry, db: Session, amount: float, user_portfolio_id: str):
    """
    :param user_entry:
    :param db: Session
    :param amount: Float
    :param user_portfolio_id: UUID
    :return: Response
    """
    user_entry = DailyReturnEntry(
        id=user_entry.id,
        last_price=user_entry.last_price,
        added_on=user_entry.added_on,
        portfolio_id=user_portfolio_id
    )
    db.add(user_entry)
    db.commit()
    db.refresh(user_entry)
    return user_entry
