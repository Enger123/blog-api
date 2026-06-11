from fastapi import APIRouter
from fastapi.params import Depends

from auth.jwt import get_current_user
from crud import likes
router = APIRouter()

@router.get("/likes/{username}")
def get_likes_username(username: str):
    return likes.get_likes_username(username)

@router.post("/posts/{post_id}/like")
def add_post_like(post_id: int, current_user=Depends(get_current_user)):
    return likes.add_post_like(post_id, current_user)

@router.delete("/posts/{post_id}/like")
def delete_post_like(post_id: int, current_user=Depends(get_current_user)):
    return likes.delete_post_like(post_id, current_user)

@router.get("/posts/{post_id}/likes")
def get_post_id_likes(post_id: int):
    return likes.get_post_id_likes(post_id)

@router.get("/users/{user_id}/likes")
def get_users_id_likes(user_id: int):
    return likes.get_users_id_likes(user_id)