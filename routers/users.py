from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserResponse, UserUpdate
from crud import users
from auth.jwt import get_current_user
from auth import jwt
from fastapi.params import Depends
from typing import List
router =  APIRouter()

@router.post("/users")
def add_user(user: UserCreate):
    return users.add_user(user)

@router.get("/me", response_model=UserResponse)
def profile(user = Depends(get_current_user)):
    return user

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    return jwt.login_for_access_token(form_data)

@router.get("/users", response_model=List[UserResponse])
def get_users() -> List[UserResponse]:
    return users.get_users()

@router.get("/users/{id}", response_model=UserResponse)
def get_user_id(id: int) -> UserResponse:
    return users.get_user_id(id)

@router.put("/users", response_model=UserResponse)
def change_user(creds: UserUpdate, current_user = Depends(get_current_user)) -> UserResponse:
    return users.change_user(creds, current_user)

@router.delete("/users", response_model=dict)
def delete_user(current_user = Depends(get_current_user)) -> dict:
    return users.delete_user(current_user)