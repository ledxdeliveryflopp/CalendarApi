from sqlalchemy import Column, Integer, String
from database.database import Base


class UserModel(Base):
    """Таблица пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(16), index=True, nullable=False, comment='Имя пользователя')
    hashed_password = Column(String, nullable=False, comment='хэшированный пароль')
