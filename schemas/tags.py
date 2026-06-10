from pydantic import BaseModel

class TagResponse(BaseModel):
    id: int
    name: str

class TagCreate(BaseModel):
    name: str