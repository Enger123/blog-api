from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class AuthorSchema(BaseModel):
    id: int
    username: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    comments_count: int
    created_at: datetime
    user: AuthorSchema

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostInfo(BaseModel):
    id: int
    title: str
    model_config = {'from_attributes': True}