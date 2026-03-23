import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from backend.app.routers.user.model import UserModel


@pytest.mark.anyio
async def test_signup_user_success(client: AsyncClient, db_session: Session):
    form_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "full_name": "New User",
        "password": "testpassword123",
    }

    response = await client.post("/api/v1/users/signup", data=form_data)

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == f"User {form_data['username']} created"
    assert data["user"]["username"] == form_data["username"]
    assert data["user"]["email"] == form_data["email"]
    assert data["user"]["full_name"] == form_data["full_name"]
    assert data["user"]["disabled"] is False

    created_user = (
        db_session.query(UserModel)
        .filter(UserModel.username == form_data["username"])
        .first()
    )
    assert created_user is not None
    assert created_user.email == form_data["email"]


@pytest.mark.anyio
async def test_signup_user_duplicate_email_returns_400(
    client: AsyncClient,
    test_user,
):
    form_data = {
        "username": "different_username",
        "email": test_user.email,
        "full_name": "Another User",
        "password": "testpassword123",
    }

    response = await client.post("/api/v1/users/signup", data=form_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.anyio
async def test_signup_user_duplicate_username_returns_400(
    client: AsyncClient,
    test_user,
):
    form_data = {
        "username": test_user.username,
        "email": "anotheremail@example.com",
        "full_name": "Another User",
        "password": "testpassword123",
    }

    response = await client.post("/api/v1/users/signup", data=form_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


@pytest.mark.anyio
async def test_signup_user_missing_field_returns_422(client: AsyncClient):
    form_data = {
        "username": "incompleteuser",
        "email": "incomplete@example.com",
        "password": "testpassword123",
    }

    response = await client.post("/api/v1/users/signup", data=form_data)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_for_access_token_success(client: AsyncClient, test_user):
    form_data = {
        "username": test_user.username,
        "password": "password123",
    }

    response = await client.post("/api/v1/users/token", data=form_data)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_for_access_token_wrong_password_returns_401(
    client: AsyncClient,
    test_user,
):
    form_data = {
        "username": test_user.username,
        "password": "wrongpassword",
    }

    response = await client.post("/api/v1/users/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


@pytest.mark.anyio
async def test_login_for_access_token_unknown_user_returns_401(client: AsyncClient):
    form_data = {
        "username": "unknownuser",
        "password": "password123",
    }

    response = await client.post("/api/v1/users/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


@pytest.mark.anyio
async def test_login_for_access_token_missing_password_returns_422(
    client: AsyncClient,
):
    form_data = {
        "username": "someuser",
    }

    response = await client.post("/api/v1/users/token", data=form_data)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_read_users_me_success(client: AsyncClient, test_user):
    login_response = await client.post(
        "/api/v1/users/token",
        data={"username": test_user.username, "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == test_user.username
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name
    assert data["disabled"] == test_user.disabled


@pytest.mark.anyio
async def test_read_users_me_unauthorized_without_token(client: AsyncClient):
    response = await client.get("/api/v1/users/me")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_read_users_me_invalid_token_returns_401(client: AsyncClient):
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalidtoken"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


@pytest.mark.anyio
async def test_read_users_me_inactive_user_returns_400(
    client: AsyncClient,
    inactive_user,
):
    login_response = await client.post(
        "/api/v1/users/token",
        data={"username": inactive_user.username, "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}


@pytest.mark.anyio
async def test_read_own_items_success(client: AsyncClient, test_user):
    login_response = await client.post(
        "/api/v1/users/token",
        data={"username": test_user.username, "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me/items",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"owner": test_user.username}


@pytest.mark.anyio
async def test_read_own_items_unauthorized_without_token(client: AsyncClient):
    response = await client.get("/api/v1/users/me/items")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_read_own_items_with_auth_client(auth_client: AsyncClient, test_user):
    response = await auth_client.get("/api/v1/users/me/items")

    assert response.status_code == 200
    assert response.json() == {"owner": test_user.username}
