import models
from sqlalchemy.orm import Session
from schemas import DailyReturnEntry
from pydantic import UUID4


def get_latest_price(db: Session, entry_id: UUID4):
    """
    :param db: Session
    :param entry_id: UUID4
    :return:
    """
    fetched_entry = db.query(models.DailyReturn).get(entry_id)
    response = {"message": "success",
                "status_code": None,
                "data": {}
                }
    if not fetched_entry:
        response['status_code'] = 404
        response['error'] = 'No entry found with given ID'
        response['id'] = entry_id
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
