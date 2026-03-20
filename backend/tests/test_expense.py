import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from backend.app.routers.expense.model import ExpenseModel


TEST_EXPENSE_NAME = "test_expense_rollback_check"


@pytest.mark.anyio
async def test_create_item_success(auth_client: AsyncClient, db_session: Session):
    form_data = {"name": TEST_EXPENSE_NAME, "amount": "3.0"}
    response = await auth_client.post("/create_expense", data=form_data)

    assert response.status_code == 200
    assert response.json() == {"message": f"Expense {form_data['name']} created"}

    created_expense = (
        db_session.query(ExpenseModel)
        .filter(ExpenseModel.name == TEST_EXPENSE_NAME)
        .first()
    )
    assert created_expense is not None
    assert created_expense.amount == 3.0


@pytest.mark.anyio
async def test_create_item_failure(auth_client: AsyncClient):
    form_data = {"name": TEST_EXPENSE_NAME}

    response = await auth_client.post("/create_expense", data=form_data)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_expense_was_rolled_back(db_session: Session):
    created_expense = (
        db_session.query(ExpenseModel)
        .filter(ExpenseModel.name == TEST_EXPENSE_NAME)
        .first()
    )

    assert created_expense is None


@pytest.mark.anyio
async def test_delete_expense_success(
    auth_client: AsyncClient,
    db_session: Session,
    test_user,
):
    expense = ExpenseModel(
        name="delete_me",
        amount=12.5,
        user_id=test_user.user_id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    response = await auth_client.delete(f"/delete_expense/{expense.expense_id}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Expense {expense.expense_id} was deleted"}

    deleted_expense = (
        db_session.query(ExpenseModel)
        .filter(ExpenseModel.expense_id == expense.expense_id)
        .first()
    )
    assert deleted_expense is None


@pytest.mark.anyio
async def test_delete_expense_other_users_expense_returns_404(
    auth_client: AsyncClient,
    db_session: Session,
    other_user,
):
    other_users_expense = ExpenseModel(
        name="not_my_expense",
        amount=50.0,
        user_id=other_user.user_id,
    )
    db_session.add(other_users_expense)
    db_session.commit()
    db_session.refresh(other_users_expense)

    response = await auth_client.delete(
        f"/delete_expense/{other_users_expense.expense_id}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}

    still_exists = (
        db_session.query(ExpenseModel)
        .filter(ExpenseModel.expense_id == other_users_expense.expense_id)
        .first()
    )
    assert still_exists is not None


@pytest.mark.anyio
async def test_delete_expense_nonexistent_id_returns_404(auth_client: AsyncClient):
    response = await auth_client.delete("/delete_expense/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}


@pytest.mark.anyio
async def test_find_expense_success(
    auth_client: AsyncClient,
    db_session: Session,
    test_user,
):
    expense1 = ExpenseModel(
        name="groceries",
        amount=20.0,
        user_id=test_user.user_id,
    )
    expense2 = ExpenseModel(
        name="groceries",
        amount=35.0,
        user_id=test_user.user_id,
    )
    expense3 = ExpenseModel(
        name="rent",
        amount=1000.0,
        user_id=test_user.user_id,
    )

    db_session.add_all([expense1, expense2, expense3])
    db_session.commit()
    db_session.refresh(expense1)
    db_session.refresh(expense2)

    response = await auth_client.get("/find_expense", params={"name": "groceries"})

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Found the following items"
    assert len(data["data"]) == 2
    assert all(item["name"] == "groceries" for item in data["data"])


@pytest.mark.anyio
async def test_find_expense_returns_only_current_users_expenses(
    auth_client: AsyncClient,
    db_session: Session,
    test_user,
    other_user,
):
    my_expense = ExpenseModel(
        name="shared_name",
        amount=10.0,
        user_id=test_user.user_id,
    )
    other_expense = ExpenseModel(
        name="shared_name",
        amount=99.0,
        user_id=other_user.user_id,
    )

    db_session.add_all([my_expense, other_expense])
    db_session.commit()
    db_session.refresh(my_expense)

    response = await auth_client.get("/find_expense", params={"name": "shared_name"})

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Found the following items"
    assert len(data["data"]) == 1
    assert data["data"][0]["user_id"] == test_user.user_id
    assert data["data"][0]["name"] == "shared_name"


@pytest.mark.anyio
async def test_find_expense_no_matches(auth_client: AsyncClient):
    response = await auth_client.get("/find_expense", params={"name": "does_not_exist"})

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Found the following items"
    assert data["data"] == []


@pytest.mark.anyio
async def test_get_all_expenses_success(
    auth_client: AsyncClient,
    db_session: Session,
    test_user,
    other_user,
):
    expense1 = ExpenseModel(
        name="coffee",
        amount=5.0,
        user_id=test_user.user_id,
    )
    expense2 = ExpenseModel(
        name="lunch",
        amount=15.0,
        user_id=test_user.user_id,
    )
    other_expense = ExpenseModel(
        name="other_user_item",
        amount=999.0,
        user_id=other_user.user_id,
    )

    db_session.add_all([expense1, expense2, other_expense])
    db_session.commit()

    response = await auth_client.get("/get_all_expenses")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == f"Found items for user {test_user.user_id}"
    assert len(data["data"]) == 2
    returned_names = {item["name"] for item in data["data"]}
    assert returned_names == {"coffee", "lunch"}


@pytest.mark.anyio
async def test_get_all_expenses_empty(auth_client: AsyncClient, test_user):
    response = await auth_client.get("/get_all_expenses")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == f"Found items for user {test_user.user_id}"
    assert data["data"] == []


@pytest.mark.anyio
async def test_update_expense_success(
    auth_client: AsyncClient,
    db_session: Session,
    test_user,
):
    expense = ExpenseModel(
        name="old_name",
        amount=10.0,
        user_id=test_user.user_id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    payload = {
        "expense_id": expense.expense_id,
        "name": "new_name",
        "amount": 25.5,
    }

    response = await auth_client.put("/update_expense", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": f"Updated expense ID {expense.expense_id}"}

    updated_expense = (
        db_session.query(ExpenseModel)
        .filter(ExpenseModel.expense_id == expense.expense_id)
        .first()
    )
    assert updated_expense is not None
    assert updated_expense.name == "new_name"
    assert updated_expense.amount == 25.5


@pytest.mark.anyio
async def test_update_expense_does_not_update_other_users_expense(
    auth_client: AsyncClient,
    db_session: Session,
    other_user,
):
    expense = ExpenseModel(
        name="protected_expense",
        amount=40.0,
        user_id=other_user.user_id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    payload = {
        "expense_id": expense.expense_id,
        "name": "hacked_name",
        "amount": 1.0,
    }

    response = await auth_client.put("/update_expense", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}

    unchanged_expense = (
        db_session.query(ExpenseModel)
        .filter(ExpenseModel.expense_id == expense.expense_id)
        .first()
    )
    assert unchanged_expense is not None
    assert unchanged_expense.name == "protected_expense"
    assert unchanged_expense.amount == 40.0


@pytest.mark.anyio
async def test_update_expense_nonexistent_id_returns_404(auth_client: AsyncClient):
    payload = {
        "expense_id": 999999,
        "name": "does_not_exist",
        "amount": 123.45,
    }

    response = await auth_client.put("/update_expense", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}
