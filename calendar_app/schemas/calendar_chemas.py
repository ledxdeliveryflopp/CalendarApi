from datetime import date
from typing import Optional
from pydantic import BaseModel


class TaskSearch(BaseModel):
    title: str

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    """Базовая модель задачи"""
    title: str
    current_datetime: date

    class Config:
        orm_mode = True


class TaskDetail(TaskBase):
    """Модель вывода полной информации о задачи"""
    id: int
    description: Optional[str] = None
    deadline_datetime: date

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    description: Optional[str] = None
    deadline_datetime: date
    user_id: int

    class Config:
        orm_mode = True
