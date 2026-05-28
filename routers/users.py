from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserCreate, UserResponse
from crud import users
from auth.jwt import get_current_user
from auth import jwt
from fastapi.params import Depends
router =  APIRouter()

@router.post("/users")
def add_user(user: UserCreate):
    return users.add_user(user)

@router.get("/me", response_model=UserResponse)
def profile(user = Depends(get_current_user)):
    return users.profile(user)

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    return jwt.login_for_access_token(form_data)