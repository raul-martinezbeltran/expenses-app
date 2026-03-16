from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase
import datetime as dt

class Base(DeclarativeBase):
    pass

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=True, default=dt.datetime.now(dt.timezone.utc))