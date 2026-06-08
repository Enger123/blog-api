from pydantic import BaseModel, Field
from datetime import datetime
from schemas.post import PostInfo, AuthorSchema

class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=100)

class CommentResponse(BaseModel):
    id: int
    text: str
    user: AuthorSchema
    post: PostInfo
    created_at: datetime

class CommentUpdate(BaseModel):
    text: str | None = None

