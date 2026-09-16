from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from schemas.post import PostResponse, PostCreate, PostUpdate
from typing import List
from app.dependencies import CurrentUser, PostServiceDep, PaginationDep
from app.background_tasks import add_post_log, delete_post_log, change_post_log
import asyncio
import time

router = APIRouter()

@router.get("/posts/tag/{tag}",
            response_model=List[PostResponse],
            tags=['Posts'])
async def get_posts_tag(tag: str, post_service: PostServiceDep) -> List[PostResponse]:
    return await post_service.get_posts_tag(tag)

@router.post("/posts",
             response_model=PostResponse,
            tags=['Posts'])
async def add_post(newpost: PostCreate,
             current_user : CurrentUser,
             post_service: PostServiceDep,
             back_tasks: BackgroundTasks) -> PostResponse:
    # back_tasks.add_task(add_post_log, newpost.title, current_user.username)
    return await post_service.add_post(newpost, current_user)

@router.post("/posts/{id}/image")
async def add_post_image(id: int, post_service: PostServiceDep,
                   current_user: CurrentUser,
                   file: UploadFile = File()):
    return await post_service.add_post_image(id, current_user, file)

@router.delete("/posts/{id}/image")
async def delete_post_image(id: int, post_service: PostServiceDep,
                   current_user: CurrentUser):
    return await post_service.delete_post_image(id, current_user)


@router.get("/posts",
            response_model=List[PostResponse],
            tags=['Posts'])
async def get_posts(post_service: PostServiceDep, skip: int = 0,
              limit: int = 10,
              title: str = None,
              sort: str = 'asc') -> List[PostResponse]:
    return await post_service.get_posts(skip, limit, title, sort)

@router.get("/all-posts")
async def posts_without_sets(post_service: PostServiceDep):
    return await post_service.get_posts_without_settings()

@router.get("/posts/by-usernane/{username}",
            response_model=List[PostResponse],
            tags=['Posts'])
async def get_posts_username(username : str, post_service: PostServiceDep) -> List[PostResponse]:
    return await post_service.get_posts_username(username)

@router.get("/posts/{id}",
            response_model=PostResponse,
            tags=['Posts'])
async def get_post_id(id: int, post_service: PostServiceDep) -> PostResponse:
    return await post_service.get_post_id(id)

@router.put("/posts/{id}",
            response_model=PostResponse,
            tags=['Posts'])
async def change_post(id: int,
                changed_post: PostUpdate,
                current_user: CurrentUser,
                post_service: PostServiceDep,
                back_tasks: BackgroundTasks) -> PostResponse:
    # back_tasks.add_task(change_post_log, id, current_user.username)
    return await post_service.change_post(id, changed_post, current_user)

@router.delete("/posts/{id}",
            tags=['Posts'])
async def delete_post(id: int,
                current_user: CurrentUser,
                post_service: PostServiceDep,
                back_tasks: BackgroundTasks) -> dict:
    back_tasks.add_task(delete_post_log, id, current_user.username)
    return await post_service.delete_post(id, current_user)

@router.get("/me/posts",
            response_model=List[PostResponse],
            tags=['Posts'])
async def my_posts(current_user: CurrentUser,
                   post_service: PostServiceDep) -> List[PostResponse]:
    return await post_service.my_posts(current_user)

@router.get("/users/{user_id}/posts",
            response_model=List[PostResponse],
            tags=['Posts'])
async def user_id_posts(user_id: int, post_service: PostServiceDep) -> List[PostResponse]:
    return await post_service.user_id_posts(user_id)

@router.get("/posts/params/e",
            tags=['Posts'])
async def posts_params(pagination: PaginationDep, post_service: PostServiceDep):
    return await post_service.posts_params(pagination)

@router.get("/sleep")
async def sleep():
    await asyncio.sleep(10)
    return {'res': 'async func completed after sleep'}

@router.get("/time")
def now():
    return {'time': time.time()}