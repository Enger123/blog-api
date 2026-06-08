from fastapi import APIRouter
from fastapi.params import Depends
from auth.jwt import get_current_user
from schemas.post import PostResponse, PostCreate, PostUpdate
from crud import posts
from typing import List

router = APIRouter()

@router.post("/posts", response_model=PostResponse)
def add_post(newpost: PostCreate, current_user = Depends(get_current_user)) -> PostResponse:
    return posts.add_post(newpost, current_user)

@router.get("/posts", response_model=List[PostResponse])
def get_posts(skip: int = 0, limit: int = 10, title: str = None, sort: str = 'asc') -> List[PostResponse]:
    return posts.get_posts(skip, limit, title, sort)

@router.get("/posts/{id}", response_model=PostResponse)
def get_post_id(id: int) -> PostResponse:
    return posts.get_post_id(id)

@router.put("/posts/{id}", response_model=PostResponse)
def change_post(id: int, changed_post: PostUpdate, current_user=Depends(get_current_user)) -> PostResponse:
    return posts.change_post(id, changed_post, current_user)

@router.delete("/posts/{id}")
def delete_post(id: int, current_user=Depends(get_current_user)) -> dict:
    return posts.delete_post(id, current_user)

@router.get("/me/posts", response_model=List[PostResponse])
def my_posts(current_user=Depends(get_current_user)) -> List[PostResponse]:
    return posts.my_posts(current_user)

@router.get("/users/{user_id}/posts", response_model=List[PostResponse])
def user_id_posts(user_id: int) -> List[PostResponse]:
    return posts.user_id_posts(user_id)