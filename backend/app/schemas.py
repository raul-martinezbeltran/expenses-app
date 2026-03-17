from pydantic import BaseModel
import datetime as dt

### Expenses
class ExpenseBase(BaseModel):
    id: int | None = None
    name: str
    amount: float

### Tokens
class TokenBase(BaseModel):
    access_token: str
    token_type: str

class TokenDataBase(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    id: int | None = None
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDBBase(UserBase):
    hashed_password: str