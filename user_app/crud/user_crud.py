from sqlalchemy.ext.asyncio import AsyncSession
from user_app.models.user_model import UserModel
from user_app.schemas.user_schemas import UserCreate
from user_app.utils.user_utils import get_password_hash


def create_user(session: AsyncSession, user_schemas: UserCreate):
    """Функция создания пользователя"""
    # password = get_password_hash(user_schemas.hashed_password)
    new_user = UserModel(username=user_schemas.username, hashed_password=get_password_hash(
        user_schemas.hashed_password))
    # new_user = UserModel(**user_schemas.model_dump(), hashed_password=hashed_password)
    session.add(new_user)
    return new_user
