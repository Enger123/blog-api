from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserResponse
from sqlalchemy import select
from typing import List
from models import Post, Like, User
from datetime import datetime
from auth.jwt import hash_password

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, newuser: UserCreate):
        return (await self.db.scalars(
            select(User)
            .where(User.username==newuser.username)
        )).first()

    def add_user(self, newuser: UserCreate):
        user = User(
            username=newuser.username,
            hashed_password=hash_password(newuser.password),
            created_at=datetime.now()
        )
        self.db.add(user)
        return user

    async def get_users(self):
        return (await self.db.scalars(
            select(User)
        )).all()

    async def get_user_by_id(self, user_id: int):
        return (await self.db.scalars(
            select(User)
            .where(User.id==user_id)
        )).first()

    async def get_current_user(self, current_user):
        return (await self.db.scalars(
            select(User)
            .where(User.id == current_user.id)
        )).first()

    async def get_users_likedpost(self, title: str):
        return (await self.db.scalars(select(User)
                    .join(Like)
                    .join(Post)
                    .where(Post.title.contains(title))
        )).all()
