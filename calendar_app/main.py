from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from crud.calendar_crud import get_all_task, create_task, get_task_by_title
from schemas.calendar_chemas import TaskDetail, TaskCreate
from database.db import async_session, engine, Base


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

calendar_app = FastAPI()


@calendar_app.on_event("startup")
async def init_tables():
    """Создаем таблицы бд"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@calendar_app.get("/list/", response_model=list[TaskDetail], tags=['Task'])
async def get_task_router(session: AsyncSession = Depends(get_session)):
    """руотер вывода всех задач"""
    tasks = await get_all_task(session)
    if not tasks:
        raise HTTPException(status_code=404, detail="Задач нет")
    return tasks


@calendar_app.get("/task/", response_model=TaskDetail, tags=['Task'])
async def get_task_by_title_router(title: str, session: AsyncSession = Depends(get_session)):
    """руотер вывода всех задач"""
    task = await get_task_by_title(session, title=title)
    if not task:
        raise HTTPException(status_code=404, detail="Задач нет")
    return task


@calendar_app.post("/create/", response_model=TaskDetail, tags=['Task'])
async def create_task_router(task_schemas: TaskCreate, session: AsyncSession = Depends(get_session)):
    """руотер создания задачи"""
    task = create_task(session=session, task_schemas=task_schemas)
    if task.current_datetime > task.deadline_datetime:
        raise HTTPException(status_code=400, detail="Срок выполнения не может быть меньше даты "
                                                    "создания")
    else:
        await session.commit()
    return task
