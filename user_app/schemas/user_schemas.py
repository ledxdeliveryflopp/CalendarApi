from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str


class UserCreate(UserBase):
    """Схема создания пользователя"""
    hashed_password: str = Field(min_length=8)


class UserFullSchemas(UserCreate):
    """Схема полной информации о пользователе"""
    id: int


class UserLogin(UserBase):
    """Схема авторизации пользователя"""
    plain_password: str


