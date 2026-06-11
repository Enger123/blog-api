from pydantic import BaseModel

from schemas.post import AuthorSchema, PostInfo


class LikeResponse(BaseModel):
    id: int
    post: PostInfo
    user: AuthorSchema
