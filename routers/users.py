from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserResponse, UserUpdate
from crud import users
from fastapi.params import Depends
from auth import jwt
from typing import List
from app.dependencies import CurrentUser, DBSession
router =  APIRouter()

@router.get("/users/likedpost/{title}",
            response_model=List[UserResponse],
            tags=['Users'])
def get_users_likedpost(title: str, db: DBSession) -> List[UserResponse]:
    return users.get_users_likedpost(title, db)

@router.post("/users",
            tags=['Users'])
def add_user(user: UserCreate, db: DBSession):
    return users.add_user(user, db)

@router.get("/me",
            response_model=UserResponse,
            tags=['Users'])
def profile(user : CurrentUser):
    return user

@router.post("/token",
            tags=['Users'])
def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    return jwt.login_for_access_token(form_data)

@router.get("/users",
            response_model=List[UserResponse],
            tags=['Users'])
def get_users(db: DBSession) -> List[UserResponse]:
    return users.get_users(db)

@router.get("/users/{id}",
            response_model=UserResponse,
            tags=['Users'])
def get_user_id(id: int, db: DBSession) -> UserResponse:
    return users.get_user_id(id, db)

@router.put("/users",
            response_model=UserResponse,
            tags=['Users'])
def change_user(creds: UserUpdate,
                current_user : CurrentUser,
                db: DBSession) -> UserResponse:
    return users.change_user(creds, current_user, db)

@router.delete("/users",
               response_model=dict,
            tags=['Users'])
def delete_user(current_user : CurrentUser,
                db: DBSession) -> dict:
    return users.delete_user(current_user, db)