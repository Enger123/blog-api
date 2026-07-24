from fastapi import APIRouter
from typing import List
from crud import comments
from app.dependencies import CurrentUser, DBSession
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter()

@router.get("/comments/user/{username}",
            response_model=List[CommentResponse],
            tags=['Comments']
            )
async def get_comments_username(username: str, db: DBSession) -> List[CommentResponse]:
    return await comments.get_comments_username(username, db)

@router.post("/posts/{id}/comments",
             response_model=CommentResponse,
            tags=['Comments'])
async def add_post_comment(id: int, newcomment: CommentCreate, current_user: CurrentUser, db: DBSession) -> CommentResponse:
    return await comments.add_post_comment(id, newcomment, current_user, db)

@router.get("/posts/{post_id}/comments",
            response_model=List[CommentResponse],
            tags=['Comments'])
async def get_post_comments(post_id: int, db: DBSession) -> List[CommentResponse]:
    return await comments.get_post_comments(post_id, db)

@router.delete("/comments/{comment_id}",
            tags=['Comments'])
async def delete_com(comment_id: int, current_user: CurrentUser, db: DBSession):
    return await comments.delete_com(comment_id, current_user, db)

@router.put("/comments/{comment_id}",
            tags=['Comments'])
async def change_com(comment_id: int, com: CommentUpdate, current_user: CurrentUser, db: DBSession):
    return await comments.change_com(comment_id, com, current_user, db)