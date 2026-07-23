from fastapi import HTTPException
from typing import List
from schemas.user import UserCreate, UserResponse, UserUpdate
from models import User, Post, Like
from datetime import datetime
from auth.jwt import hash_password
from sqlalchemy import select

async def get_users_likedpost(title: str, db) -> List[UserResponse]:
    # users = db.query(User)\
    #     .join(Like)\
    #     .join(Post)\
    #     .filter(Post.title.contains(title)).all()
    db_query = await db.execute(select(User)
                                .join(Like)
                                .join(Post)
                                .where(Post.title.contains(title))
                                )
    users = db_query.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail='Users not found who liked this post')
    return [UserResponse.model_validate(user) for user in users]

async def add_user(newuser: UserCreate, db):
    db_query = await db.execute(select(User).where(User.username==newuser.username))
    username = db_query.scalars().first()
    if username:
        raise HTTPException(status_code=403, detail='User already exists')
    user = User(
            username = newuser.username,
            hashed_password=hash_password(newuser.password),
            created_at=datetime.now()
        )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)

async def get_users(db) -> List[UserResponse]:
    db_query = await db.execute(select(User).order_by(User.id.asc()))
    users = db_query.scalars().all()
    return [UserResponse.model_validate(user)
                for user in users]

async def get_user_id(id: int, db) -> UserResponse:
    db_query = await db.execute(select(User).where(User.id==id))
    user = db_query.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserResponse.model_validate(user)

async def change_user(creds: UserUpdate, current_user, db) -> UserResponse:
    db_query = await db.execute(select(User).where(User.id==current_user.id))
    user_to_change = db_query.scalars().first()
    if not user_to_change:
        raise HTTPException(status_code=404, detail='User not found')
    if creds.username is not None:
        user_to_change.username = creds.username
    if creds.password is not None:
        user_to_change.hashed_password = hash_password(creds.password)
    await db.commit()
    await db.refresh(user_to_change)
    return UserResponse.model_validate(user_to_change)

async def delete_user(current_user, db) -> dict:
    db_query = await db.execute(select(User).where(User.id==current_user.id))
    user_to_del = db_query.scalars().first()
    if not user_to_del:
        raise HTTPException(status_code=404, detail='Use not found')
    await db.delete(user_to_del)
    await db.commit()
    return {'message': 'deleted'}





