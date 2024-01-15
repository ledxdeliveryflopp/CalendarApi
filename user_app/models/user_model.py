from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class UserModel(Base):
    """Таблица пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(16), unique=True, index=True, nullable=False, comment='Имя '
                                                                                   'пользователя')
    hashed_password = Column(String, nullable=False, comment='хэшированный пароль')


class TokenModel(Base):
    """Таблица токенов"""
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String, nullable=False, comment='Токен')
    type = Column(String, default="bearer", comment='Тип токена')
    expires = Column(DateTime, comment='Время жизни токена')
    user_id = Column(Integer, ForeignKey("users.id"), comment='Владелец токена')

    user = relationship(UserModel)
