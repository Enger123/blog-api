from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

db = create_async_engine(
    "postgresql+asyncpg://postgres:Enger123@localhost:5432/blog_api")
Session = async_sessionmaker(bind=db)
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
