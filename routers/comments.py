from fastapi import APIRouter
from typing import List
from app.dependencies import CurrentUser, CommentServiceDep
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter()

@router.get("/comments/user/{username}",
            response_model=List[CommentResponse],
            tags=['Comments']
            )
async def get_comments_username(username: str,
                                comment_service: CommentServiceDep) -> List[CommentResponse]:
    return await comment_service.get_comments_username(username)

@router.post("/posts/{post_id}/comments",
             response_model=CommentResponse,
            tags=['Comments'])
async def add_post_comment(post_id: int,
                           newcomment: CommentCreate,
                           current_user: CurrentUser,
                           comment_service: CommentServiceDep) -> CommentResponse:
    return await comment_service.add_post_comment(post_id,
                                                  newcomment,
                                                  current_user)

@router.get("/posts/{post_id}/comments",
            response_model=List[CommentResponse],
            tags=['Comments'])
async def get_post_comments(post_id: int,
                            comment_service: CommentServiceDep) -> List[CommentResponse]:
    return await comment_service.get_post_comments(post_id)

@router.delete("/comments/{comment_id}",
            tags=['Comments'])
async def delete_com(comment_id: int,
                     current_user: CurrentUser,
                     comment_service: CommentServiceDep):
    return await comment_service.delete_com(comment_id,
                                            current_user)

@router.put("/comments/{comment_id}",
            tags=['Comments'])
async def change_com(comment_id: int,
                     com: CommentUpdate,
                     current_user: CurrentUser,
                     comment_service: CommentServiceDep):
    return await comment_service.change_com(comment_id,
                                            com,
                                            current_user)