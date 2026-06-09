from pydantic import BaseModel

class TagResponse(BaseModel):
    id: int
    name: str
    post_id: int

class TagCreate(BaseModel):
    name: str