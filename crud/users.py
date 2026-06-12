from fastapi import HTTPException
from typing import List
from schemas.user import UserCreate, UserResponse, UserUpdate
from app.database import Session
from models import User, Post, Like
from datetime import datetime
from auth.jwt import hash_password

def get_users_likedpost(title: str) -> List[UserResponse]:
    with Session() as session:
        users = session.query(User)\
        .join(Like)\
        .join(Post)\
        .filter(Post.title.contains(title)).all()
        if not users:
            raise HTTPException(status_code=404, detail='Users not found who liked this post')
        return [UserResponse.model_validate(user) for user in users]

def add_user(newuser: UserCreate):
    with Session() as session:
        username = session.query(User).filter_by(username=newuser.username).first()
        if username:
            raise HTTPException(status_code=403, detail='User already exists')
        user = User(
            username = newuser.username,
            hashed_password=hash_password(newuser.password),
            created_at=datetime.now()
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse.model_validate(user)

def get_users() -> List[UserResponse]:
    with Session() as session:
        users = session.query(User).all()
        return [UserResponse.model_validate(user)
                for user in users]

def get_user_id(id: int) -> UserResponse:
    with Session() as session:
        user = session.query(User).filter_by(id=id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return UserResponse.model_validate(user)

def change_user(creds: UserUpdate, current_user) -> UserResponse:
    with Session() as session:
        user_to_change = session.query(User).filter_by(id=current_user.id).first()
        if not user_to_change:
            raise HTTPException(status_code=404, detail='User not found')
        if creds.username is not None:
            user_to_change.username = creds.username
        if creds.password is not None:
            user_to_change.hashed_password = hash_password(creds.password)
        session.commit()
        return UserResponse.model_validate(user_to_change)

def delete_user(current_user) -> dict:
    with Session() as session:
        user_to_del = session.query(User).filter_by(id=current_user.id).first()
        if not user_to_del:
            raise HTTPException(status_code=404, detail='Use not found')
        session.delete(user_to_del)
        session.commit()
        return {'message': 'deleted'}





