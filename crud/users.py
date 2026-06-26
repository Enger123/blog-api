from fastapi import HTTPException
from typing import List
from schemas.user import UserCreate, UserResponse, UserUpdate
from app.database import Session
from models import User, Post, Like
from datetime import datetime
from auth.jwt import hash_password

def get_users_likedpost(title: str, db) -> List[UserResponse]:
    users = db.query(User)\
        .join(Like)\
        .join(Post)\
        .filter(Post.title.contains(title)).all()
    if not users:
        raise HTTPException(status_code=404, detail='Users not found who liked this post')
    return [UserResponse.model_validate(user) for user in users]

def add_user(newuser: UserCreate, db):
    username = db.query(User).filter_by(username=newuser.username).first()
    if username:
        raise HTTPException(status_code=403, detail='User already exists')
    user = User(
            username = newuser.username,
            hashed_password=hash_password(newuser.password),
            created_at=datetime.now()
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

def get_users(db) -> List[UserResponse]:
    users = db.query(User).all()
    return [UserResponse.model_validate(user)
                for user in users]

def get_user_id(id: int, db) -> UserResponse:
    user = db.query(User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserResponse.model_validate(user)

def change_user(creds: UserUpdate, current_user, db) -> UserResponse:
    user_to_change = db.query(User).filter_by(id=current_user.id).first()
    if not user_to_change:
        raise HTTPException(status_code=404, detail='User not found')
    if creds.username is not None:
        user_to_change.username = creds.username
    if creds.password is not None:
        user_to_change.hashed_password = hash_password(creds.password)
    db.commit()
    return UserResponse.model_validate(user_to_change)

def delete_user(current_user, db) -> dict:
    user_to_del = db.query(User).filter_by(id=current_user.id).first()
    if not user_to_del:
        raise HTTPException(status_code=404, detail='Use not found')
    db.delete(user_to_del)
    db.commit()
    return {'message': 'deleted'}





