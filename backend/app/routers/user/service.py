from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from backend.app.service_database import get_db
from backend.app.routers.user.model import UserModel
from backend.app.schemas import (
    UserBase,
    UserInDBBase,
    TokenDataBase,
    TokenBase,
    UserCreateBase,
)
import os

load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["Users"])

SessionDep = Annotated[Session, Depends(get_db)]


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return password_hash.hash(password)


def get_user(username: str, session: SessionDep) -> UserInDBBase | None:
    try:
        user_model = (
            session.query(UserModel)
            .filter(UserModel.username == username)
            .one_or_none()
        )
        if user_model:
            user_base = UserInDBBase(
                id=user_model.user_id,
                username=user_model.username,
                email=user_model.email,
                full_name=user_model.full_name,
                disabled=user_model.disabled,
                hashed_password=user_model.hashed_password,
            )

            return user_base
        return None
    except Exception as e:
        return {"message": f"Error occurred {e}"}


def authenticate_user(username: str, password: str, session: SessionDep):
    user_model = get_user(username, session)

    if not user_model:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user_model.hashed_password):
        return False

    return user_model


def create_access_token(data: dict, expires_delta: Annotated[timedelta, None] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenDataBase(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username, session)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@router.post("/signup")
async def signup_user(user_in: UserCreateBase, session: SessionDep):
    try:
        user_model = (
            session.query(UserModel)
            .filter(UserModel.email == user_in.email)
            .one_or_none()
        )
        if user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user_model = (
            session.query(UserModel)
            .filter(UserModel.username == user_in.username)
            .one_or_none()
        )
        if user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        hashed_password = get_password_hash(user_in.password)
        user_model = UserModel(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            disabled=False,
        )

        session.add(user_model)
        session.commit()
        return {"message": f"User {user_in.username} created"}
    except Exception as e:
        return {"message": f"Error ocurred {e}"}


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> TokenBase:
    user = authenticate_user(
        username=form_data.username, password=form_data.password, session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return TokenBase(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
) -> UserBase:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
):

    return [{"owner": current_user.username}]
