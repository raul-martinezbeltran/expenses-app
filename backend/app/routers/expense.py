from fastapi import APIRouter, Form, Depends, Path, Query
from typing import Annotated
from sqlalchemy.orm import Session

from app.service_database import get_db
from app.model import ExpenseModel
from app.schemas import ExpenseBase

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db)]

@router.post("/create_expense")
async def create_expense(expense: Annotated[ExpenseBase, Form()], session: SessionDep):
    try:
        expense_model = ExpenseModel(name=expense.name, amount=expense.amount)
        session.add(expense_model)
        session.commit()
        return {"message": f"Expense {expense.name} created"}
    except Exception as e:
        return {"message": f"{e}"}
    
@router.delete("delete_expense/{id}")
async def delete_expense(id: Annotated[int, Path(title="The ID of the expense to delete")], session: SessionDep):
    try:
        session.query(ExpenseModel).filter(ExpenseModel.id == id).delete()
        session.commit()
        return {"message": f"Expense {id} was deleted"}
    except Exception as e:
        return {"message": f"Error occurred"}