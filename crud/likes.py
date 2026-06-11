from fastapi import HTTPException
from schemas.post import PostResponse, AuthorSchema, PostInfo
from models import Like, Post, User
from app.database import Session
from datetime import datetime

from schemas.user import UserResponse
from schemas.like import LikeResponse

def get_likes_username(username: str):
    with Session() as session:
        likes = session.query(Like).join(User).filter(User.username.contains(username)).all()
        if not likes:
            raise HTTPException(status_code=404, detail='Likes not found from this user')
        return [LikeResponse(id=l.id,
                             user=AuthorSchema(id=l.user_id,
                                               username=l.user.username
                                               ),
                             post=PostInfo(id=l.post_id,
                                           title=l.post.title)
                             )
                for l in likes]

def add_post_like(post_id: int, current_user):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        existing_like = session.query(Like).filter_by(user_id=current_user.id, post_id=post_id).first()
        if existing_like:
            raise HTTPException(status_code=400, detail='You already liked this post')

        like = Like(user_id=current_user.id, post_id=post_id)
        session.add(like)
        session.commit()
        session.refresh(like)
        return PostResponse(id=post_id,
                            title=post.title,
                            content=post.content,
                            comments_count=len(post.comments),
                            likes_count=len(post.likes),
                            created_at=post.created_at,
                            user=AuthorSchema(id=post.user.id, username=post.user.username)
                            )

def delete_post_like(post_id: int, current_user):
    with Session() as session:
        like = session.query(Like).filter_by(post_id=post_id, user_id=current_user.id).first()
        if not like:
            raise HTTPException(status_code=404, detail='Post not found')
        session.delete(like)
        session.commit()
        return {'message': 'Лайк прибрано'}

def get_post_id_likes(post_id: int):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        likes = post.likes
        return [UserResponse(id=like.user.id,
                             username=like.user.username,
                             created_at=like.user.created_at
                             ) for like in likes]

def get_users_id_likes(user_id: int):
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return [PostResponse(id = like.post.id,
                             title=like.post.title,
                             content=like.post.content,
                             comments_count=len(like.post.comments),
                             likes_count=len(like.post.likes),
                             created_at=like.post.created_at,
                             user=AuthorSchema(id=user_id,
                                               username=user.username
                                               ))
                for like in user.likes]

