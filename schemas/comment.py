from pydantic import BaseModel
from datetime import datetime
from schemas.post import PostInfo, AuthorSchema

class CommentCreate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    id: int
    text: str
    user: AuthorSchema
    post: PostInfo
    created_at: datetime
    model_config = {'from_attributes': True}

class CommentUpdate(BaseModel):
    text: str | None = None

