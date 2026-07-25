from fastapi import HTTPException
from crud.posts import POST_ROAD_OPTIONS, post_returning
from schemas.post import PostResponse, AuthorSchema, PostInfo
from models import Like, Post, User
from schemas.user import UserResponse
from schemas.like import LikeResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload

LIKES_ROAD_OPTIONS = (
    selectinload(Like.user),
    selectinload(Like.post)

)

async def get_likes_username(username: str, db):
    likes_query = await db.execute(select(Like)
                             .join(User)
                             .where(User.username.contains(username))
                             .options(*LIKES_ROAD_OPTIONS)
                                   )
    likes = likes_query.scalars().all()
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

async def add_post_like(post_id: int, current_user, db):
    post_query = await db.execute(select(Post)
                            .where(Post.id==post_id)
                            .options(
        *POST_ROAD_OPTIONS
    )
                             )
    post = post_query.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')

    existing_like_query = await db.execute(select(Like)
            .where(Like.user_id==current_user.id,
                   Like.post_id==post_id))
    existing_like = existing_like_query.scalars().first()
    if existing_like:
        raise HTTPException(status_code=400, detail='You already liked this post')

    like = Like(user_id=current_user.id, post_id=post_id)
    db.add(like)
    await db.commit()
    await db.refresh(like)
    await db.refresh(post)
    return post_returning(post)

async def delete_post_like(post_id: int, current_user, db):
    like_query = await db.execute(select(Like)
            .where(post_id=post_id, user_id=current_user.id))
    like = like_query.scalars().first()
    if not like:
        raise HTTPException(status_code=404, detail='Post not found')
    await db.delete(like)
    await db.commit()
    return {'message': 'Лайк прибрано'}

async def get_post_id_likes(post_id: int, db):
    post_query = await db.execute(select(Post)
                            .where(Post.id==post_id)
                            .options(selectinload(Post.likes).selectinload(Like.user))
                            )
    post = post_query.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    likes = post.likes
    return [UserResponse(id=like.user.id,
                             username=like.user.username,
                             created_at=like.user.created_at
                             ) for like in likes]

async def get_users_id_likes(user_id: int, db):
    user_query = await db.execute(select(User)
                            .where(User.id==user_id)
                            .options(selectinload(User.likes)
                                     .selectinload(Like.post)
                                     .selectinload(Post.likes),
                                     selectinload(User.likes)
                                     .selectinload(Like.post)
                                     .selectinload(Post.comments)
                                     )
                            )
    user = user_query.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return [PostResponse(id = like.post.id,
                             title=like.post.title,
                             content=like.post.content,
                            user_id=like.post.user_id,
                            image_path=like.post.image_path,
                             comments_count=len(like.post.comments),
                             likes_count=len(like.post.likes),
                             created_at=like.post.created_at,
                             user=AuthorSchema(id=user_id,
                                               username=user.username
                                               ))
                for like in user.likes]

