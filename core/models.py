import uuid
from sqlalchemy import Column, Date, Float, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class User(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key=True)


class Portfolio(Base):
    __tablename__ = 'database_projects_portfolio'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_name = Column(String)
    created_on = Column(Date)
    user = Column(ForeignKey("auth_user.id"))


class DailyReturn(Base):
    __tablename__ = 'database_projects_dailyreturn'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_price = Column(Float)
    added_on = Column(Date)
    portfolio_id = Column(ForeignKey("database_projects_portfolio.id"))
