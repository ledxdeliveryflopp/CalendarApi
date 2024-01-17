from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.cart_model import CartModel


async def get_all_cart(session: AsyncSession):
    """Функция вывода всех корзин"""
    result = await session.execute(select(CartModel))
    return result.scalars().all()


def create_cart(session: AsyncSession, user_id: int, products_id: list):
    """Функция создания товара"""
    new_cart = CartModel(products=products_id, user_id=user_id)
    session.add(new_cart)
    return new_cart
