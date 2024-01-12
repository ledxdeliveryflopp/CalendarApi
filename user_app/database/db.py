from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


engine = create_async_engine(
    'postgresql+asyncpg://postgres:postgres@postgres:5432/postgres', echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

