from fastapi import APIRouter
from app.dependencies import CurrentUser, LikeServiceDep

router = APIRouter()

@router.get("/likes/{username}", tags=['Likes'])
async def get_likes_username(username: str,
                       like_service: LikeServiceDep
                             ):
    return await like_service.get_likes_username(username)

@router.post("/posts/{post_id}/like", tags=['Likes'])
async def add_post_like(post_id: int,
                        current_user: CurrentUser,
                        like_service: LikeServiceDep):
    return await like_service.add_post_like(post_id, current_user)

@router.delete("/posts/{post_id}/like", tags=['Likes'])
async def delete_post_like(post_id: int,
                           current_user: CurrentUser,
                           like_service: LikeServiceDep):
    return await like_service.delete_post_like(post_id, current_user)

@router.get("/posts/{post_id}/likes", tags=['Likes'])
async def get_post_id_likes(post_id: int,
                            like_service: LikeServiceDep):
    return await like_service.get_post_id_likes(post_id)

@router.get("/users/{user_id}/likes", tags=['Likes'])
async def get_users_id_likes(user_id: int,
                             like_service: LikeServiceDep):
    return await like_service.get_users_id_likes(user_id)