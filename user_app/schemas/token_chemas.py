from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    """Схема токена"""
    token: str
    expires: datetime
    user_id: int


class TokenData(BaseModel):
    """Схема токена для получения пользователя"""
    user_id: int
