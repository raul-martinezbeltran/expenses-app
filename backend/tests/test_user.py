import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from backend.app.routers.user.model import UserModel
from backend.app.routers.user.service import get_password_hash


@pytest.mark.anyio
async def test_signup_user_success(client: AsyncClient, db_session: Session):
    form_data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "full_name": "New User",
        "password": "test_password_123",
    }

    response = await client.post("/signup", data=form_data)

    assert response.status_code == 200
    assert response.json() == {"message": f"User {form_data['username']} created"}

    created_user = (
        db_session.query(UserModel)
        .filter(UserModel.username == form_data["username"])
        .first()
    )
    assert created_user is not None
    assert created_user.email == form_data["email"]
    assert created_user.full_name == form_data["full_name"]
    assert created_user.disabled is False
    assert created_user.hashed_password != form_data["password"]


@pytest.mark.anyio
async def test_signup_user_duplicate_email_returns_400(
    client: AsyncClient, db_session: Session
):
    existing_user = UserModel(
        username="existing_user",
        email="duplicate@example.com",
        full_name="Existing User",
        hashed_password=get_password_hash("password123"),
        disabled=False,
    )
    db_session.add(existing_user)
    db_session.commit()

    form_data = {
        "username": "different_username",
        "email": "duplicate@example.com",
        "full_name": "Another User",
        "password": "test_password_123",
    }

    response = await client.post("/signup", data=form_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.anyio
async def test_signup_user_duplicate_username_returns_400(
    client: AsyncClient, db_session: Session
):
    existing_user = UserModel(
        username="duplicate_user",
        email="existing@example.com",
        full_name="Existing User",
        hashed_password=get_password_hash("password123"),
        disabled=False,
    )
    db_session.add(existing_user)
    db_session.commit()

    form_data = {
        "username": "duplicate_user",
        "email": "new_email@example.com",
        "full_name": "Another User",
        "password": "test_password_123",
    }

    response = await client.post("/signup", data=form_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


@pytest.mark.anyio
async def test_signup_user_missing_field_returns_422(client: AsyncClient):
    form_data = {
        "username": "incomplete_user",
        "email": "incomplete@example.com",
        "password": "test_password_123",
    }

    response = await client.post("/signup", data=form_data)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_for_access_token_success(client: AsyncClient, db_session: Session):
    password = "correct_password"
    user = UserModel(
        username="login_user",
        email="login_user@example.com",
        full_name="Login User",
        hashed_password=get_password_hash(password),
        disabled=False,
    )
    db_session.add(user)
    db_session.commit()

    form_data = {
        "username": "login_user",
        "password": password,
    }

    response = await client.post("/token", data=form_data)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert len(body["access_token"]) > 0


@pytest.mark.anyio
async def test_login_for_access_token_wrong_password_returns_401(
    client: AsyncClient, db_session: Session
):
    user = UserModel(
        username="wrong_password_user",
        email="wrong_password@example.com",
        full_name="Wrong Password User",
        hashed_password=get_password_hash("correct_password"),
        disabled=False,
    )
    db_session.add(user)
    db_session.commit()

    form_data = {
        "username": "wrong_password_user",
        "password": "incorrect_password",
    }

    response = await client.post("/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


@pytest.mark.anyio
async def test_login_for_access_token_unknown_user_returns_401(client: AsyncClient):
    form_data = {
        "username": "missing_user",
        "password": "some_password",
    }

    response = await client.post("/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


@pytest.mark.anyio
async def test_login_for_access_token_missing_password_returns_422(
    client: AsyncClient,
):
    form_data = {
        "username": "login_user",
    }

    response = await client.post("/token", data=form_data)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_read_users_me_success(client: AsyncClient, db_session: Session):
    password = "me_password"
    user = UserModel(
        username="me_user",
        email="me_user@example.com",
        full_name="Me User",
        hashed_password=get_password_hash(password),
        disabled=False,
    )
    db_session.add(user)
    db_session.commit()

    token_response = await client.post(
        "/token",
        data={"username": "me_user", "password": password},
    )
    token = token_response.json()["access_token"]

    response = await client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "me_user"
    assert body["email"] == "me_user@example.com"
    assert body["full_name"] == "Me User"
    assert body["disabled"] is False


@pytest.mark.anyio
async def test_read_users_me_unauthorized_without_token(client: AsyncClient):
    response = await client.get("/users/me/")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_read_users_me_invalid_token_returns_401(client: AsyncClient):
    response = await client.get(
        "/users/me/",
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


@pytest.mark.anyio
async def test_read_users_me_inactive_user_returns_400(
    client: AsyncClient, db_session: Session
):
    password = "inactive_password"
    user = UserModel(
        username="inactive_user",
        email="inactive_user@example.com",
        full_name="Inactive User",
        hashed_password=get_password_hash(password),
        disabled=True,
    )
    db_session.add(user)
    db_session.commit()

    token_response = await client.post(
        "/token",
        data={"username": "inactive_user", "password": password},
    )
    token = token_response.json()["access_token"]

    response = await client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}


@pytest.mark.anyio
async def test_read_own_items_success(client: AsyncClient, db_session: Session):
    password = "items_password"
    user = UserModel(
        username="items_user",
        email="items_user@example.com",
        full_name="Items User",
        hashed_password=get_password_hash(password),
        disabled=False,
    )
    db_session.add(user)
    db_session.commit()

    token_response = await client.post(
        "/token",
        data={"username": "items_user", "password": password},
    )
    token = token_response.json()["access_token"]

    response = await client.get(
        "/users/me/items/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"owner": "items_user"}


@pytest.mark.anyio
async def test_read_own_items_unauthorized_without_token(client: AsyncClient):
    response = await client.get("/users/me/items/")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_read_own_items_with_auth_client(auth_client: AsyncClient):
    response = await auth_client.get("/users/me/items/")

    assert response.status_code == 200
    assert response.json() == {"owner": "test_user"}
