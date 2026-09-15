from fastapi import APIRouter
from app.dependencies import CurrentUser, TagServiceDep
from schemas.tag_post import TagPostResponse
from schemas.tags import TagCreate, TagResponse
from typing import List

router = APIRouter()

@router.get("/tags/postliked/{username}",
            response_model=List[TagResponse],
            tags=['Tags'])
async def get_tags_postliked(username: str,
                             tag_service: TagServiceDep) -> List[TagResponse]:
    return await tag_service.get_tags_postliked(username)

@router.get("/tags/user/{username}",
            response_model=List[TagResponse],
            tags=['Tags'])
async def get_tags_inpost_username(username: str,
                                   tag_service: TagServiceDep) -> List[TagResponse]:
    return await tag_service.get_tags_inpost_username(username)

@router.post("/tags",
             response_model=TagResponse,
            tags=['Tags'])
async def create_tag(newtag: TagCreate, tag_service: TagServiceDep) -> TagResponse:
    return await tag_service.create_tag(newtag)

@router.get("/tags",
            response_model=List[TagResponse],
            tags=['Tags'])
async def get_tags(tag_service: TagServiceDep) -> List[TagResponse]:
    return await tag_service.get_tags()

@router.get("/posts/{post_id}/tags",
            response_model=List[TagPostResponse],
            tags=['Tags'])
async def get_post_tags(post_id: int, tag_service: TagServiceDep):
    return await tag_service.get_post_tags(post_id)

@router.post("/posts/{post_id}/tags/{tag_id}",
             response_model=TagPostResponse,
            tags=['Tags'])
async def add_post_tags(post_id: int,
                        tag_id: int,
                        current_user: CurrentUser,
                        tag_service: TagServiceDep):
    return await tag_service.add_post_tags(post_id,
                                           tag_id,
                                           current_user)

@router.delete("/posts/{post_id}/tags/{tag_id}",
               response_model=dict,
            tags=['Tags'])
async def delete_post_tags(post_id: int,
                           tag_id: int,
                           current_user: CurrentUser,
                           tag_service: TagServiceDep) -> dict:
    return await tag_service.delete_post_tags(post_id,
                                              tag_id,
                                              current_user)