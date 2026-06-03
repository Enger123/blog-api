from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6, max_length=100)

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    model_config = {'from_attributes': True}