from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.database import Base


class UserModel(Base):
    """Таблица пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(16), index=True, nullable=False, comment='Имя пользователя')
    hashed_password = Column(String, nullable=False, comment='хэшированный пароль')


class TokenModel(Base):
    """Таблица токенов"""
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String, nullable=False)
    expires = Column(DateTime())
    user_id = Column(Integer, ForeignKey("users.id"))
