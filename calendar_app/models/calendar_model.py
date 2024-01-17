from sqlalchemy import Column, Integer, String, Date
from database.db import Base


class TaskModel(Base):
    """Таблица задач"""
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(16), index=True, nullable=False, comment='Название задачи')
    description = Column(String(160), comment='Описание задачи')
    current_datetime = Column(Date, nullable=False, comment='Время создания задачи')
    deadline_datetime = Column(Date, nullable=False, comment='Срок выполнения')
    user_id = Column(Integer, nullable=False)


