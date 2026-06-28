from fastapi import APIRouter
from app.dependencies import CurrentUser, DBSession
from crud import likes
router = APIRouter()

@router.get("/likes/{username}", tags=['Likes'])
def get_likes_username(username: str,
                       db: DBSession):
    return likes.get_likes_username(username, db)

@router.post("/posts/{post_id}/like", tags=['Likes'])
def add_post_like(post_id: int, current_user: CurrentUser, db: DBSession):
    return likes.add_post_like(post_id, current_user, db)

@router.delete("/posts/{post_id}/like", tags=['Likes'])
def delete_post_like(post_id: int, current_user: CurrentUser, db: DBSession):
    return likes.delete_post_like(post_id, current_user, db)

@router.get("/posts/{post_id}/likes", tags=['Likes'])
def get_post_id_likes(post_id: int, db: DBSession):
    return likes.get_post_id_likes(post_id, db)

@router.get("/users/{user_id}/likes", tags=['Likes'])
def get_users_id_likes(user_id: int, db: DBSession):
    return likes.get_users_id_likes(user_id, db)