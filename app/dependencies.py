from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from auth.jwt import get_current_user
from fastapi.params import Depends
from schemas.post import PaginationParams
from models import User
from app.database import get_db
from crud import PostService, TagService, UserService, CommentService, LikeService

CurrentUser = Annotated[User, Depends(get_current_user)]
PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]
DBSession = Annotated[AsyncSession, Depends(get_db)]

def get_post_service(db: DBSession):
    return PostService(db)

def get_user_service(db: DBSession):
    return UserService(db)

def get_like_service(db: DBSession):
    return LikeService(db)

def get_comment_service(db: DBSession):
    return CommentService(db)

def get_tag_service(db: DBSession):
    return TagService(db)

PostServiceDep = Annotated[PostService, Depends(get_post_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
LikeServiceDep = Annotated[LikeService, Depends(get_like_service)]
CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]
TagServiceDep = Annotated[TagService, Depends(get_tag_service)]