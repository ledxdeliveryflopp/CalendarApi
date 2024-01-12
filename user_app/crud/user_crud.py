from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_app.models.user_model import UserModel
from user_app.schemas.user_schemas import UserCreate
from user_app.utils.user_utils import get_password_hash


async def get_all_user(session: AsyncSession):
    """Функция вывода всех пользователей"""
    result = await session.execute(select(UserModel))
    return result.scalars().all()


def create_user(session: AsyncSession, user_schemas: UserCreate):
    """Функция создания пользователя"""
    new_user = UserModel(username=user_schemas.username, hashed_password=get_password_hash(
        user_schemas.hashed_password))
    session.add(new_user)
    return new_user


async def get_user(session: AsyncSession, username: str):
    """Функция вывода пользователя по username"""
    user = await session.execute(select(UserModel).where(UserModel.username == username))
    return user.scalars().first()

