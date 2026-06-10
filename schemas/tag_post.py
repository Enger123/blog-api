from pydantic import BaseModel

class TagPostResponse(BaseModel):
    id: int
    tag_id: int
    post_id: int
    tag_name: str
    post_title: str