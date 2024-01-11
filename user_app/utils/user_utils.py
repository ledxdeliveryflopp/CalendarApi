from passlib.context import CryptContext
from user_app.models.user_model import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Функция проверки пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Функция хэширования пароля"""
    return pwd_context.hash(password)
