import random
import string
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from crud.user_crud import get_user_id
from models.user_model import TokenModel
from schemas.token_chemas import TokenData

SECRET_KEY = "7c0a6642516997c4ec8afa5613192c47bac0ab758b17ed1c14893d1a99d1e449"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(session: AsyncSession, user_id: int):
    """Функция создания токена"""
    data = {}
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    random_string = random.choices(string.ascii_lowercase, k=10)
    to_encode.update({"exp": expire, "user_id": user_id, "random_string": random_string})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    new_token = TokenModel(token=encoded_jwt, expires=expire, user_id=user_id)
    session.add(new_token)
    return new_token


async def get_all_token(session: AsyncSession):
    """Функция вывода всех токенов"""
    tokens = await session.execute(select(TokenModel))
    return tokens.scalars().all()


async def get_token_by_user_id(session: AsyncSession, user_id: int):
    """Функция вывода всех токенов"""
    token = await session.execute(select(TokenModel).where(TokenModel.user_id == user_id))
    return token.scalars().first()


async def get_user_by_token(session: AsyncSession, token: str):
    """Функция вывода текущего пользователя по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    token_data = TokenData(user_id=user_id)
    user = await get_user_id(session, user_id=token_data.user_id)
    return user

