from fastapi import APIRouter
from typing import List
from crud import comments
from auth.jwt import get_current_user
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from fastapi.params import Depends

router = APIRouter()

@router.get("/comments/user/{username}", response_model=List[CommentResponse])
def get_comments_username(username: str) -> List[CommentResponse]:
    return comments.get_comments_username(username)

@router.post("/posts/{id}/comments", response_model=CommentResponse)
def add_post_comment(id: int, newcomment: CommentCreate, current_user=Depends(get_current_user)) -> CommentResponse:
    return comments.add_post_comment(id, newcomment, current_user)

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_post_comments(post_id: int) -> List[CommentResponse]:
    return comments.get_post_comments(post_id)

@router.delete("/comments/{comment_id}")
def delete_com(comment_id: int, current_user=Depends(get_current_user)):
    return comments.delete_com(comment_id, current_user)

@router.put("/comments/{comment_id}")
def change_com(comment_id: int, com: CommentUpdate, current_user=Depends(get_current_user)):
    return comments.change_com(comment_id, com, current_user)