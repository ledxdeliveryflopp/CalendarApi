from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from calendar_app.models.calendar_model import TaskModel
from calendar_app.schemas.calendar_chemas import TaskCreate


async def get_all_task(session: AsyncSession):
    """Функция вывода всех задач"""
    result = await session.execute(select(TaskModel))
    return result.scalars().all()


async def get_task_by_title(session: AsyncSession, title: str):
    """Функция вывода задач с определенным названием"""
    result = await session.execute(select(TaskModel).where(TaskModel.title == title))
    return result.first()


def create_task(session: AsyncSession, task_schemas: TaskCreate):
    """Функция создания задачи"""
    new_task = TaskModel(**task_schemas.model_dump())
    session.add(new_task)
    return new_task
