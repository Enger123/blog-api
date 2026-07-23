from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from schemas.post import PostResponse, PostCreate, PostUpdate
from crud import posts
from typing import List
from app.dependencies import CurrentUser, DBSession, PaginationDep
from app.background_tasks import add_post_log, delete_post_log, change_post_log
import asyncio
import time
router = APIRouter()

@router.get("/posts/tag/{tag}",
            response_model=List[PostResponse],
            tags=['Posts'])
def get_posts_tag(tag: str, db: DBSession) -> List[PostResponse]:
    return posts.get_posts_tag(tag, db)

@router.post("/posts",
             response_model=PostResponse,
            tags=['Posts'])
async def add_post(newpost: PostCreate,
             current_user : CurrentUser,
             db: DBSession,
             back_tasks: BackgroundTasks) -> PostResponse:
    # back_tasks.add_task(add_post_log, newpost.title, current_user.username)
    return await posts.add_post(newpost, current_user, db)

@router.post("/posts/{id}/image")
async def add_post_image(id: int, db: DBSession,
                   current_user: CurrentUser,
                   file: UploadFile = File()):
    return await posts.add_post_image(id, db, current_user, file)

@router.delete("/posts/{id}/image")
async def delete_post_image(id: int, db: DBSession,
                   current_user: CurrentUser):
    return await posts.delete_post_image(id, db, current_user)


@router.get("/posts",
            response_model=List[PostResponse],
            tags=['Posts'])
async def get_posts(db: DBSession, skip: int = 0,
              limit: int = 10,
              title: str = None,
              sort: str = 'asc') -> List[PostResponse]:
    return await posts.get_posts(db, skip, limit, title, sort)

@router.get("/posts/by-usernane/{username}",
            response_model=List[PostResponse],
            tags=['Posts'])
async def get_posts_username(username : str, db: DBSession) -> List[PostResponse]:
    return await posts.get_posts_username(username, db)

@router.get("/posts/{id}",
            response_model=PostResponse,
            tags=['Posts'])
async def get_post_id(id: int, db: DBSession) -> PostResponse:
    return await posts.get_post_id(id, db)

@router.put("/posts/{id}",
            response_model=PostResponse,
            tags=['Posts'])
async def change_post(id: int,
                changed_post: PostUpdate,
                current_user: CurrentUser,
                db: DBSession,
                back_tasks: BackgroundTasks) -> PostResponse:
    # back_tasks.add_task(change_post_log, id, current_user.username)
    return await posts.change_post(id, changed_post, current_user, db)

@router.delete("/posts/{id}",
            tags=['Posts'])
async def delete_post(id: int,
                current_user: CurrentUser,
                db: DBSession,
                back_tasks: BackgroundTasks) -> dict:
    # back_tasks.add_task(delete_post_log, id, current_user.username)
    return await posts.delete_post(id, current_user, db)

@router.get("/me/posts",
            response_model=List[PostResponse],
            tags=['Posts'])
async def my_posts(current_user: CurrentUser, db: DBSession) -> List[PostResponse]:
    return await posts.my_posts(current_user, db)

@router.get("/users/{user_id}/posts",
            response_model=List[PostResponse],
            tags=['Posts'])
async def user_id_posts(user_id: int, db: DBSession) -> List[PostResponse]:
    return await posts.user_id_posts(user_id, db)

@router.get("/posts/params/e",
            tags=['Posts'])
async def posts_params(pagination: PaginationDep, db: DBSession):
    return await posts.posts_params(pagination, db)

@router.get("/sleep")
async def sleep():
    await asyncio.sleep(10)
    return {'res': 'async func completed after sleep'}

@router.get("/time")
def now():
    return {'time': time.time()}