from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserResponse, UserUpdate
from fastapi.params import Depends
from auth import jwt
from typing import List
from app.dependencies import CurrentUser, UserServiceDep, get_db
from app.background_tasks import add_user_log

router =  APIRouter(tags=['Users'])

@router.get("/server/stats")
def counter(request: Request):
    return {
        'general requests': request.app.state.stats['requests'],
        'users': request.app.state.stats['users'],
        'posts': request.app.state.stats['posts'],
        'tags': request.app.state.stats['tags'],
        'stats': request.app.state.stats['stats'],
        'likes': request.app.state.stats['likes'],
        'comments': request.app.state.stats['comments']
    }

@router.get("/users/likedpost/{title}",
            response_model=List[UserResponse])
async def get_users_likedpost(title: str, user_service: UserServiceDep) -> List[UserResponse]:
    return await user_service.get_users_likedpost(title)

@router.post("/users")
async def add_user(user: UserCreate, user_service: UserServiceDep, back_tasks: BackgroundTasks):
    # back_tasks.add_task(add_user_log, user.username)
    return await user_service.add_user(user)

@router.get("/me",
            response_model=UserResponse)
def profile(user : CurrentUser):
    return user

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(),
                                 db: AsyncSession=Depends(get_db)):
    return await jwt.login_for_access_token(form_data, db)

@router.get("/users",
            response_model=List[UserResponse]
)
async def get_users(user_service: UserServiceDep,
              ) -> List[UserResponse]:
    return await user_service.get_users()

@router.get("/users/{id}",
            response_model=UserResponse)
async def get_user_id(id: int, user_service: UserServiceDep) -> UserResponse:
    return await user_service.get_user_id(id)

@router.put("/users",
            response_model=UserResponse)
async def change_user(creds: UserUpdate,
                current_user : CurrentUser,
                user_service: UserServiceDep) -> UserResponse:
    return await user_service.change_user(creds, current_user)

@router.delete("/users",
               response_model=dict)
async def delete_user(current_user : CurrentUser,
                user_service: UserServiceDep) -> dict:
    return await user_service.delete_user(current_user)