from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.database import get_db
import models
from app.database import Base
import asyncio


test_db = create_async_engine(
    "postgresql+asyncpg://postgres:Enger123@localhost:5432/blog_api_test",
    poolclass=NullPool
)
TestSession = async_sessionmaker(bind=test_db, expire_on_commit=False)

async def get_test_db():
    async with TestSession() as test_session:
        yield test_session

app.dependency_overrides[get_db] = get_test_db

# async def create_tables():
#     async with test_db.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# asyncio.run(create_tables())