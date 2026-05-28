from fastapi import HTTPException
from schemas.user import UserCreate, UserResponse
from app.database import Session
from models.user_model import User
from datetime import datetime
from auth.jwt import hash_password

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
        return UserResponse(id=user.id, username=user.username, created_at=user.created_at)

def profile(current_user):
    return current_user
