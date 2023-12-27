from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from calendar_app.models.calendar_model import TaskModel
from calendar_app.schemas.calendar_chemas import TaskCreate


async def get_all_task(session: AsyncSession):
    """Функция вывода всех задач"""
    result = await session.execute(select(TaskModel))
    return result.scalars().all()


async def get_calendar_by_task(db: AsyncSession, task: str):
    """Функция вывода задач с определенным названием"""
    result = await db.query(TaskModel).filter(TaskModel.task == task).first()
    return result


def create_task(session: AsyncSession, task_schemas: TaskCreate):
    """Функция создания задачи"""
    new_task = TaskModel(**task_schemas.model_dump())
    session.add(new_task)
    return new_task
