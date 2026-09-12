from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from crud.posts import PostService
from auth.jwt import get_current_user
from fastapi.params import Depends
from schemas.post import PaginationParams
from models import User
from app.database import get_db

CurrentUser = Annotated[User, Depends(get_current_user)]
PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]
DBSession = Annotated[AsyncSession, Depends(get_db)]

def get_post_service(db: DBSession):
    return PostService(db)

PostServiceDep = Annotated[PostService, Depends(get_post_service)]
