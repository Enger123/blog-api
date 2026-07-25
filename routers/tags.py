from fastapi import APIRouter
from app.dependencies import CurrentUser, DBSession
from crud import tags
from schemas.tag_post import TagPostResponse
from schemas.tags import TagCreate, TagResponse
from typing import List

router = APIRouter()

@router.get("/tags/postliked/{username}",
            response_model=List[TagResponse],
            tags=['Tags'])
async def get_tags_postliked(username: str, db: DBSession) -> List[TagResponse]:
    return await tags.get_tags_postliked(username, db)

@router.get("/tags/user/{username}",
            response_model=List[TagResponse],
            tags=['Tags'])
async def get_tags_inpost_username(username: str, db: DBSession) -> List[TagResponse]:
    return await tags.get_tags_inpost_username(username, db)

@router.post("/tags",
             response_model=TagResponse,
            tags=['Tags'])
async def create_tag(newtag: TagCreate, db: DBSession) -> TagResponse:
    return await tags.create_tag(newtag, db)

@router.get("/tags",
            response_model=List[TagResponse],
            tags=['Tags'])
async def get_tags(db: DBSession) -> List[TagResponse]:
    return await tags.get_tags(db)

@router.get("/posts/{post_id}/tags",
            response_model=List[TagPostResponse],
            tags=['Tags'])
async def get_post_tags(post_id: int, db: DBSession):
    return await tags.get_post_tags(post_id, db)

@router.post("/posts/{post_id}/tags/{tag_id}",
             response_model=TagPostResponse,
            tags=['Tags'])
async def add_post_tags(post_id: int, tag_id: int, current_user: CurrentUser, db: DBSession):
    return await tags.add_post_tags(post_id, tag_id, current_user, db)

@router.delete("/posts/{post_id}/tags/{tag_id}",
               response_model=dict,
            tags=['Tags'])
async def delete_post_tags(post_id: int, tag_id: int, current_user: CurrentUser, db: DBSession) -> dict:
    return await tags.delete_post_tags(post_id, tag_id, current_user, db)