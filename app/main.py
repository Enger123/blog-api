from fastapi import FastAPI
from app.database import Base, db
import models
from routers.users import router as users_router

app = FastAPI()
app.include_router(users_router)
Base.metadata.create_all(bind=db)