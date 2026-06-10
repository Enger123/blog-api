from fastapi import APIRouter
from fastapi.params import Depends

from auth.jwt import get_current_user
from crud import tags
from schemas.tag_post import TagPostResponse
from schemas.tags import TagCreate, TagResponse
from typing import List

router = APIRouter()

@router.post("/tags", response_model=TagResponse)
def create_tag(newtag: TagCreate) -> TagResponse:
    return tags.create_tag(newtag)

@router.get("/tags", response_model=List[TagResponse])
def get_tags() -> List[TagResponse]:
    return tags.get_tags()

@router.get("/posts/{post_id}/tags", response_model=List[TagPostResponse])
def get_post_tags(post_id: int):
    return tags.get_post_tags(post_id)

@router.post("/posts/{post_id}/tags/{tag_id}", response_model=TagPostResponse)
def add_post_tags(post_id: int, tag_id: int, current_user=Depends(get_current_user)):
    return tags.add_post_tags(post_id, tag_id, current_user)

@router.delete("/posts/{post_id}/tags/{tag_id}", response_model=dict)
def delete_post_tags(post_id: int, tag_id: int, current_user=Depends(get_current_user)) -> dict:
    return tags.delete_post_tags(post_id, tag_id, current_user)