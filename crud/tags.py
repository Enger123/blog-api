from fastapi import HTTPException
from pygments.util import tag_re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import Post, TagPost, User, Tag, Like
from repositories import TagRepository, PostRepository
from schemas.tags import TagResponse, TagCreate
from typing import List
from schemas.tag_post import TagPostResponse
from crud.posts import post_404
from sqlalchemy import select

class TagService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tag_repository = TagRepository(db)
        self.post_repository = PostRepository(db)

    def tags_returning(self, tags):
        return [TagResponse(id=tag.id, name=tag.name) for tag in tags]

    def tag_post_returning(self, tag_post):
        return [TagPostResponse(id=t.id,
                                tag_id=t.tag.id,
                                post_id=t.post_id,
                                tag_name=t.tag.name,
                                post_title=t.post.title)
                    for t in tag_post]

    def tag_post_404(self, tag_post):
        if not tag_post:
            raise HTTPException(status_code=404, detail='Tags not found')

    async def get_tags_postliked(self, username: str) -> List[TagResponse]:
        tags = await self.tag_repository.list_tags_post_liked(username)
        if not tags:
                raise HTTPException(status_code=404,
                                    detail=f'Tags not found in the posts liked by {username}')
        return self.tags_returning(tags)

    async def get_tags_inpost_username(self, username: str) -> List[TagResponse]:
        tags = await self.tag_repository.get_tags_inpost_username(username)
        return self.tags_returning(tags)

    async def create_tag(self, newtag: TagCreate):
        tag = await self.tag_repository.create_tag(newtag)
        await self.db.commit()
        await self.db.refresh(tag)
        return TagResponse(id=tag.id,
                               name=tag.name)

    async def get_tags(self) -> List[TagResponse]:
        tags = self.tag_repository.get_tags()
        if not tags:
            raise HTTPException(status_code=404, detail='Tags not found')
        return self.tags_returning(tags)

    async def get_post_tags(self, post_id: int):
        post = await self.post_repository.get_post(post_id)
        post_404(post)
        tag_post = self.tag_repository.get_post_tags(post_id)
        self.tag_post_404(tag_post)
        return self.tag_post_returning(tag_post)

    async def add_post_tags(self,
                            post_id: int,
                            tag_id: int,
                            current_user):
        post = await self.post_repository.get_post(post_id)
        post_404(post)
        if post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='You are not the owner of this post')
        tag = await self.tag_repository.get_tag(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail='Tag not found')
        tag_post = await self.tag_repository.get_tag_post(post_id, tag_id)
        if tag_post:
            raise HTTPException(status_code=400, detail='There is the same tag in this post')
        new_tag_post = await self.tag_repository.add_tag_in_post(post_id, tag_id)
        await self.db.commit()
        await self.db.refresh(tag)
        await self.db.refresh(post)
        await self.db.refresh(new_tag_post)
        return TagPostResponse(id=new_tag_post.id,
                                   tag_id=tag.id,
                                   post_id=post.id,
                                   tag_name=tag.name,
                                   post_title=post.title
                                   )

    async def delete_post_tags(self,
                               post_id: int,
                               tag_id: int,
                               current_user) -> dict:
        post = await self.post_repository.get_post(post_id)
        post_404(post)
        if post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='You are not the owner of this post')
        tag_post = await self.tag_repository.get_tag_post(post_id, tag_id)
        self.tag_post_404(tag_post)
        await self.tag_repository.delete_post_tags(tag_post)
        await self.db.commit()
        return {'message': 'Tag deleted in the post'}