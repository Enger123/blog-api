import sqlalchemy
from sqlalchemy.orm import Mapped, declarative_base, sessionmaker, mapped_column

db = sqlalchemy.create_engine(
    "postgresql+psycopg2://postgres:Enger123@localhost:5432/blog_api"
)
Session = sessionmaker(bind=db)
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
