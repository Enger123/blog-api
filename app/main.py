from fastapi import FastAPI
from app.database import Base, db
import models
from routers.users import router as users_router
from routers.posts import router as posts_router
from routers.comments import router as comments_router

app = FastAPI()
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
Base.metadata.create_all(bind=db)