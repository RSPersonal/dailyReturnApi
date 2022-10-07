from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4


class DailyReturnEntry(BaseModel):
    id = UUID4
    last_price = float
    added_on = datetime
    portfolio_id = UUID4

    class Config:
        orm_mode = True


class DailyReturnEntryUpdate(BaseModel):
    id = Optional[UUID4]
    last_price = Optional[float]
    added_on = Optional[datetime]
    portfolio_id = Optional[UUID4]

    class Config:
        arbitrary_types_allowed = True
