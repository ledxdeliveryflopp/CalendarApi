from typing import Annotated
from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from crud.token_crud import create_access_token, get_all_token, get_user_by_token
from crud.user_crud import get_all_user, create_user, get_user, get_user_id
from schemas.token_chemas import Token
from schemas.user_schemas import UserFullSchemas, UserCreate, UserBase
from database.db import async_session, engine, Base
from utils.user_utils import verify_password


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


user_system = FastAPI()


@user_system.on_event("startup")
async def init_tables():
    """Создаем таблицы бд"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


@user_system.get("/list/", response_model=list[UserFullSchemas], tags=['User'])
async def get_all_user_router(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession =
                              Depends(get_session)):
    """руотер вывода всех пользователей"""
    users = await get_all_user(session)
    if not users:
        raise HTTPException(status_code=404, detail="Пользователей нет")
    return users


@user_system.get("/user_id/", response_model=UserFullSchemas, tags=['User'])
async def get_user_by_id(user_id: int, token: Annotated[str, Depends(oauth2_scheme)], session:
                         AsyncSession = Depends(get_session)):
    """Роутер вывода пользователя по id"""
    user = await get_user_id(session, user_id=user_id)
    return user


@user_system.post("/create/", response_model=UserFullSchemas, tags=['User'])
async def create_user_router(user_schemas: UserCreate, session: AsyncSession = Depends(get_session)):
    """Роутер создания пользователя"""
    user = create_user(session=session, user_schemas=user_schemas)
    await session.commit()
    return user


@user_system.post("/token/", tags=['Tokens'])
async def login_for_access_token_router(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                        session: AsyncSession = Depends(get_session)):
    """Роутер авторизации для получения токена"""
    user = await get_user(session=session, username=form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="Не верное имя пользователя или пароль")
    if not verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=404, detail="Не верное имя пользователя или пароль")
    access_token = create_access_token(session, user_id=user.id)
    await session.commit()
    return {"access_token": access_token.token, "token_type": "bearer"}


@user_system.get("/all_tokens/", response_model=list[Token], tags=['Tokens'])
async def all_tokens_router(session: AsyncSession = Depends(get_session)):
    """Роутер вывода всех токенов"""
    tokens = await get_all_token(session)
    return tokens


@user_system.get("/get_user/", response_model=UserBase, tags=['Tokens'])
async def get_user_router(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(
                            get_session)):
    """Роутер вывода текущего авторизированного пользователя"""
    user = get_user_by_token(session=session, token=token)
    return user

