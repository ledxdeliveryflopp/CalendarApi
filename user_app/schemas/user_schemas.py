from pydantic import BaseModel, Field

from user_app.schemas.token_chemas import Token


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str


class UserCreate(UserBase):
    """Схема создания пользователя"""
    hashed_password: str = Field(min_length=8)


class UserTestSchemas(UserCreate):
    """test"""
    id: int


class UserLogin(UserBase):
    plain_password: str


