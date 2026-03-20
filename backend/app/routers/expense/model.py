import datetime as dt

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class ExpenseModel(Base):
    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
