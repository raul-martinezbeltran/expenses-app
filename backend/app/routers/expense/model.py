from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import datetime as dt
class Base(DeclarativeBase):
    pass

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[dt.datetime] =  mapped_column(nullable=True, default=dt.datetime.now(dt.timezone.utc))