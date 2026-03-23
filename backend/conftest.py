import os

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.app.service_database import get_db
from backend.app.routers.user.service import (
    get_current_active_user,
    get_password_hash,
)
from backend.app.schemas import UserBase
from backend.app.routers.user.model import UserModel

load_dotenv()

TEST_DATABASE_URL = (
    f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/"
    f"{os.getenv('TEST_DB_NAME')}"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def reset_tables():
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM expenses"))
        connection.execute(text("DELETE FROM users"))
    yield


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
async def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def test_user(db_session):
    user = UserModel(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        disabled=False,
        hashed_password=get_password_hash("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def other_user(db_session):
    user = UserModel(
        username="other_user",
        email="other@example.com",
        full_name="Other User",
        disabled=False,
        hashed_password=get_password_hash("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def inactive_user(db_session):
    user = UserModel(
        username="inactive_user",
        email="inactive@example.com",
        full_name="Inactive User",
        disabled=True,
        hashed_password=get_password_hash("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
async def auth_client(db_session, test_user):
    def override_get_db():
        yield db_session

    def override_get_current_active_user():
        return UserBase(
            user_id=test_user.user_id,
            username=test_user.username,
            email=test_user.email,
            full_name=test_user.full_name,
            disabled=test_user.disabled,
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client

    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_active_user, None)
