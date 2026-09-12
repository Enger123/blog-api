from pydantic import BaseModel, Field
from datetime import datetime

class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    content: str = Field(min_length=3, max_length=100)

class AuthorSchema(BaseModel):
    id: int
    username: str
    model_config = {'from_attributes': True}

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    image_path: str | None = None
    comments_count: int
    likes_count: int
    created_at: datetime
    user: AuthorSchema
    model_config = {'from_attributes': True}

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostInfo(BaseModel):
    id: int
    title: str

class PaginationParams(BaseModel):
    limit: int = Field(5, ge = 3, le=100)
    offset: int = Field(0)
