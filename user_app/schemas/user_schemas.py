from pydantic import BaseModel, Field


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


