from fastapi import FastAPI
from calendar_app.router import calendar_router
from database.database import engine, Base
from user_app.router import user_router

calendar = FastAPI(title="Calendar", description="Calendar API", version="0.1")

calendar.include_router(calendar_router.router)
calendar.include_router(user_router.router)


@calendar.on_event("startup")
async def init_tables():
    """Создаем таблицы бд"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
