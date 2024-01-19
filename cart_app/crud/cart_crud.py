import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.cart_model import CartModel


async def get_all_cart(session: AsyncSession):
    """Функция вывода всех корзин"""
    result = await session.execute(select(CartModel))
    return result.scalars().all()


def create_cart(session: AsyncSession, user_id: int, products_id: list):
    """Функция создания корзины"""
    new_cart = CartModel(products=products_id, user_id=user_id)
    session.add(new_cart)
    return new_cart


async def get_user(user_id: int):
    user_url = f'http://calendarapi-user_app-1:8000/user_id/?user_id={user_id}'
    async with httpx.AsyncClient() as client:
        response = await client.get(user_url)
        if response.status_code == 500:
            raise HTTPException(status_code=500, detail='Сервер пользователей не отвечает')
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail='Пользователь на найден')
        json = response.json()
        user: int = json['id']
    return user
