import datetime
from pydantic import BaseModel, UUID4


class DailyReturnEntry(BaseModel):
    id = UUID4
    last_price = float
    added_on = datetime.time
    portfolio_id = UUID4

    class Config:
        orm_mode = True
