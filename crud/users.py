from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.users import UserRepository
from schemas.user import UserCreate, UserResponse, UserUpdate
from auth.jwt import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def get_users_likedpost(self, title: str) -> List[UserResponse]:
        users = await self.user_repository.get_users_likedpost(title)
        if not users:
            raise HTTPException(status_code=404, detail='Users not found who liked this post')
        return [UserResponse.model_validate(user) for user in users]

    async def add_user(self, newuser: UserCreate) -> UserResponse:
        username = await self.user_repository.get_user_by_username(newuser)
        if username:
            raise HTTPException(status_code=403, detail='User already exists')
        user = self.user_repository.add_user(newuser)
        await self.db.commit()
        await self.db.refresh(user)
        return UserResponse.model_validate(user)

    async def get_users(self) -> List[UserResponse]:
        users = await self.user_repository.get_users()
        return [UserResponse.model_validate(user)
                    for user in users]

    async def get_user_id(self, id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return UserResponse.model_validate(user)

    async def change_user(self, creds: UserUpdate, current_user) -> UserResponse:
        user_to_change = await self.user_repository.get_current_user(current_user)
        if not user_to_change:
            raise HTTPException(status_code=404, detail='User not found')
        if creds.username is not None:
            user_to_change.username = creds.username
        if creds.password is not None:
            user_to_change.hashed_password = hash_password(creds.password)
        await self.db.commit()
        await self.db.refresh(user_to_change)
        return UserResponse.model_validate(user_to_change)

    async def delete_user(self, current_user) -> dict:
        user_to_del = await self.user_repository.get_current_user(current_user)
        if not user_to_del:
            raise HTTPException(status_code=404, detail='User not found')
        await self.db.delete(user_to_del)
        await self.db.commit()
        return {'message': 'deleted'}





