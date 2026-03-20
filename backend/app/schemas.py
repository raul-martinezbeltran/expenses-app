from pydantic import BaseModel


### Expenses
class ExpenseCreateBase(BaseModel):
    name: str
    amount: float


class ExpenseUpdateBase(BaseModel):
    expense_id: int
    name: str
    amount: float


class ExpenseResponseBase(BaseModel):
    expense_id: int
    name: str
    amount: float
    user_id: int


### Tokens
class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenDataBase(BaseModel):
    username: str | None = None


### Users
class UserBase(BaseModel):
    user_id: int | None = None
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDBBase(UserBase):
    hashed_password: str


class UserCreateBase(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
