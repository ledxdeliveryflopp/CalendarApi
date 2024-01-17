from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from database.db import Base


class CartModel(Base):
    """Модель карзины"""
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    products = Column(ARRAY(Integer), nullable=True)
    user_id = Column(Integer, nullable=False, index=True, unique=True)
