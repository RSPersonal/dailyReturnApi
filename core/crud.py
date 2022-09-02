import models, schemas
from sqlalchemy.orm import Session


def get_latest_price(db: Session, entry_id: str):
    return db.query(models.DailyReturn)
