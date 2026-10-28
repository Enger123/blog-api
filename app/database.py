from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
import os
from core.config import settings

db = create_async_engine(
    settings.DATABASE_URL
    # , poolclass=NullPool
    )

Session = async_sessionmaker(bind=db, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with Session() as session:
        yield session

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
