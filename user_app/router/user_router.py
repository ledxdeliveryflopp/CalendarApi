from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import async_session
from user_app.crud.token_crud import create_access_token
from user_app.crud.user_crud import create_user, get_all_user, get_user
from user_app.schemas.token_chemas import Token
from user_app.schemas.user_schemas import UserTestSchemas, UserCreate
from user_app.utils.token_utils import ACCESS_TOKEN_EXPIRE_MINUTES
from user_app.utils.user_utils import verify_password


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


@router.get("/list/", response_model=list[UserTestSchemas])
async def get_user_router(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession =
                          Depends(get_session)):
    """руотер вывода всех пользователей"""
    users = await get_all_user(session)
    if not users:
        raise HTTPException(status_code=404, detail="Пользователей нет")
    return users


@router.post("/create/", response_model=UserTestSchemas)
async def create_user_router(user_schemas: UserCreate, session: AsyncSession = Depends(
                             get_session)):
    """Роутер создания пользователя"""
    user = create_user(session=session, user_schemas=user_schemas)
    await session.commit()
    return user


@router.post("/my_profile/", response_model=UserTestSchemas)
async def get_profile(form_data: OAuth2PasswordRequestForm = Depends(),
                      session: AsyncSession = Depends(get_session)):
    """test"""
    user = await get_user(session=session, username=form_data.username)
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: AsyncSession = Depends(get_session)):
    user = await get_user(session=session, username=form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="Не верное имя пользователя или пароль")
    if not verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=404, detail="Не верное имя пользователя или пароль")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
