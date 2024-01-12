from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from calendar_app.crud.calendar_crud import get_all_task, create_task, get_task_by_title
from calendar_app.schemas.calendar_chemas import TaskDetail, TaskCreate
from database.database import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


router = APIRouter(
    prefix="/calendar",
    tags=["calendar"],
)


@router.get("/list/", response_model=list[TaskDetail])
async def get_task_router(session: AsyncSession = Depends(get_session)):
    """руотер вывода всех задач"""
    tasks = await get_all_task(session)
    if not tasks:
        raise HTTPException(status_code=404, detail="Задач нет")
    return tasks


@router.get("/task/", response_model=TaskDetail)
async def get_task_by_title_router(title: str, session: AsyncSession = Depends(get_session)):
    """руотер вывода всех задач"""
    task = await get_task_by_title(session, title=title)
    if not task:
        raise HTTPException(status_code=404, detail="Задач нет")
    return task


@router.post("/create/", response_model=TaskDetail)
async def create_task_router(task_schemas: TaskCreate, session: AsyncSession = Depends(get_session)):
    """руотер создания задачи"""
    task = create_task(session=session, task_schemas=task_schemas)
    if task.current_datetime > task.deadline_datetime:
        raise HTTPException(status_code=400, detail="Срок выполнения не может быть меньше даты "
                                                    "создания")
    else:
        await session.commit()
    return task
