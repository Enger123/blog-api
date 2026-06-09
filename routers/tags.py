from fastapi import APIRouter
from crud import tags
from schemas.tags import TagCreate
router = APIRouter()

@router.get("/posts/{post_id}/tags")
def get_post_tags(post_id: int):
    return tags.get_post_tags(post_id)

@router.post("/posts/{post_id}/tags")
def add_post_tags(post_id: int, newtag: TagCreate):
    return tags.add_post_tags(post_id, newtag)