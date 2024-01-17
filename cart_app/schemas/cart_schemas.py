from typing import List, Optional

from pydantic import BaseModel


class Cart(BaseModel):
    """Схема корзины"""
    products: Optional[list] = []
    user_id: int

    class Config:
        orm_mode = True
