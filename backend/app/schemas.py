from pydantic import BaseModel
import datetime as dt
from typing import Optional

class ExpenseBase(BaseModel):
    name: str
    amount: float