from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Path, status
from sqlalchemy.orm import Session

from backend.app.service_database import get_db
from backend.app.routers.expense.model import ExpenseModel
from backend.app.schemas import (
    ExpenseCreateBase,
    ExpenseResponseBase,
    ExpenseUpdateBase,
    UserBase,
)
from backend.app.routers.user.service import get_current_active_user

router = APIRouter(prefix="/api/v1/expenses")

SessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[UserBase, Depends(get_current_active_user)]


def serialize_expense(expense: ExpenseModel) -> ExpenseResponseBase:
    return ExpenseResponseBase(
        expense_id=expense.expense_id,
        name=expense.name,
        amount=expense.amount,
        user_id=expense.user_id,
    )


@router.post("/create_expense", tags=["expenses"])
async def create_expense(
    expense: Annotated[ExpenseCreateBase, Form()],
    session: SessionDep,
    current_user: CurrentUserDep,
):
    try:
        expense_model = ExpenseModel(
            name=expense.name,
            amount=expense.amount,
            user_id=current_user.user_id,
        )
        session.add(expense_model)
        session.commit()
        session.refresh(expense_model)

        return {"message": f"Expense {expense.name} created"}
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating an expense",
        )


@router.delete("/delete_expense/{id}", tags=["expenses"])
async def delete_expense(
    id: Annotated[int, Path(title="The ID of the expense to delete")],
    session: SessionDep,
    current_user: CurrentUserDep,
):
    try:
        rows_deleted = (
            session.query(ExpenseModel)
            .filter(ExpenseModel.expense_id == id)
            .filter(ExpenseModel.user_id == current_user.user_id)
            .delete()
        )

        session.commit()

        if rows_deleted == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found",
            )

        return {"message": f"Expense {id} was deleted"}
    except HTTPException:
        raise
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting expense",
        )


@router.get("/find_expense", tags=["expenses"])
async def find_expenses(
    name: str,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    try:
        expenses = (
            session.query(ExpenseModel)
            .filter(ExpenseModel.name == name)
            .filter(ExpenseModel.user_id == current_user.user_id)
            .all()
        )

        return {
            "message": "Found the following items",
            "data": [serialize_expense(expense).model_dump() for expense in expenses],
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error retrieving expense",
        )


@router.get("/get_all_expenses", tags=["expenses"])
async def get_all_expenses_from_user(
    session: SessionDep,
    current_user: CurrentUserDep,
):
    try:
        expenses = (
            session.query(ExpenseModel)
            .filter(ExpenseModel.user_id == current_user.user_id)
            .all()
        )

        return {
            "message": f"Found items for user {current_user.user_id}",
            "data": [serialize_expense(expense).model_dump() for expense in expenses],
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error retrieving expenses",
        )


@router.put("/update_expense", tags=["expenses"])
async def update_expense(
    expense: ExpenseUpdateBase,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    try:
        rows_updated = (
            session.query(ExpenseModel)
            .filter(ExpenseModel.expense_id == expense.expense_id)
            .filter(ExpenseModel.user_id == current_user.user_id)
            .update(
                {
                    "name": expense.name,
                    "amount": expense.amount,
                }
            )
        )

        session.commit()

        if rows_updated == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found",
            )

        return {"message": f"Updated expense ID {expense.expense_id}"}
    except HTTPException:
        raise
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update expense",
        )
