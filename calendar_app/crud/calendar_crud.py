from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.calendar_model import TaskModel
from schemas.calendar_chemas import TaskCreate


async def get_all_task(session: AsyncSession):
    """Функция вывода всех задач"""
    result = await session.execute(select(TaskModel))
    return result.scalars().all()


async def get_task_by_title(session: AsyncSession, title: str):
    """Функция вывода задач с определенным названием"""
    result = await session.execute(select(TaskModel).where(TaskModel.title == title))
    return result.first()


def create_task(session: AsyncSession, task_schemas: TaskCreate, user_id: int):
    """Функция создания задачи"""
    new_task = TaskModel(title=task_schemas.title, description=task_schemas.description,
                         current_datetime=task_schemas.current_datetime,
                         deadline_datetime=task_schemas.deadline_datetime, user_id=user_id)
    session.add(new_task)
    return new_task
