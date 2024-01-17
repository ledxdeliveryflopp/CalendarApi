from typing import Annotated, List, Optional, Union

import httpx
from fastapi import FastAPI, Depends, Query, HTTPException
from httpx import HTTPError
from sqlalchemy.ext.asyncio import AsyncSession
from crud.cart_crud import create_cart, get_all_cart, get_user
from database.db import async_session, engine, Base
from schemas.cart_schemas import Cart


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


cart_system = FastAPI()


@cart_system.on_event("startup")
async def init_tables():
    """Создаем таблицы бд"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@cart_system.post('/add_cart/', response_model=Cart, tags=['Cart'])
async def create_cart_router(user_id: int, products_id: list[int] = Query(None),
                             session: AsyncSession = Depends(get_session)):
    user = await get_user(user_id=user_id)
    new_cart = create_cart(session, products_id=products_id, user_id=user)
    return new_cart


@cart_system.get('/all_cart/', response_model=list[Cart], tags=['Cart'])
async def get_carts_router(session: AsyncSession = Depends(get_session)):
    carts = await get_all_cart(session)
    return carts
