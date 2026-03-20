import datetime as dt

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ExpenseModel(Base):
    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        nullable=True,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )
    user_id: Mapped[int] = mapped_column(nullable=False)
