from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from app.database import Base, db
import models
from exceptions.errors import PostNotFound
from routers.users import router as users_router
from routers.posts import router as posts_router
from routers.comments import router as comments_router
from routers.likes import router as likes_router
from routers.tags import router as tags_router
from routers.stats import router as stats_router
from contextlib import asynccontextmanager
from app.middleware import my_middleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

project_dir = Path(__file__).parent.parent
uploads = project_dir / 'uploads'

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.stats = {
        'requests': 0,
        'users': 0,
        'posts': 0,
        'tags': 0,
        'stats': 0,
        'likes': 0,
        'comments': 0
    }
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/uploads", StaticFiles(directory=uploads), name='uploads')

@app.exception_handler(PostNotFound)
async def post_not_found(request, exc):
    return JSONResponse(status_code=404,
                            content=
                            {
                                'detail': str(exc)
                            })

app.middleware('http')(my_middleware)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(tags_router)
app.include_router(stats_router)