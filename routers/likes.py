from fastapi import APIRouter
from app.dependencies import CurrentUser, DBSession
from crud import likes
router = APIRouter()

@router.get("/likes/{username}", tags=['Likes'])
async def get_likes_username(username: str,
                       db: DBSession):
    return await likes.get_likes_username(username, db)

@router.post("/posts/{post_id}/like", tags=['Likes'])
async def add_post_like(post_id: int, current_user: CurrentUser, db: DBSession):
    return await likes.add_post_like(post_id, current_user, db)

@router.delete("/posts/{post_id}/like", tags=['Likes'])
async def delete_post_like(post_id: int, current_user: CurrentUser, db: DBSession):
    return await likes.delete_post_like(post_id, current_user, db)

@router.get("/posts/{post_id}/likes", tags=['Likes'])
async def get_post_id_likes(post_id: int, db: DBSession):
    return await likes.get_post_id_likes(post_id, db)

@router.get("/users/{user_id}/likes", tags=['Likes'])
async def get_users_id_likes(user_id: int, db: DBSession):
    return await likes.get_users_id_likes(user_id, db)