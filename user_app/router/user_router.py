from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session
from user_app.crud.user_crud import create_user
from user_app.schemas.user_schemas import UserTestSchemas, UserCreate
from user_app.utils.user_utils import get_password_hash


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/create/", response_model=UserTestSchemas)
async def create_user_router(user_schemas: UserCreate, session: AsyncSession = Depends(get_session)):
    """Роутер создания пользователя"""
    user = create_user(session=session, user_schemas=user_schemas)
    await session.commit()
    return user
