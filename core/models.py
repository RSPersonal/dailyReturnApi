from sqlalchemy import Column, Date, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class DailyReturn(Base):
    __tablename__ = 'database_projects_dailyreturn'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_price = Column(Float)
    added_on = Column(Date)
    portfolio_id = Column(ForeignKey)
