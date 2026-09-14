from sqlalchemy.ext.asyncio import AsyncSession
from models import TagPost, Tag, Like, User, Post
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from schemas.tags import TagCreate

TAGPOST_ROAD_OPTIONS = (
    selectinload(TagPost.post),
    selectinload(TagPost.tag)
)


class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_tags_post_liked(self, username: str):
        return (await self.db.execute(select(Tag)
                .join(TagPost)
                .join(Post)
                .join(Like)
                .join(User)
                .where(User.username == username)
                                 )
                ).scalars().all()

    async def get_tags_inpost_username(self, username: str):
        return (await self.db.execute(select(Tag)
            .join(TagPost)
            .join(Post)
            .join(User)
            .where(User.username.contains(username)
                   )
                                 )
                ).scalars().all()

    def create_tag(self, newtag: TagCreate):
        tag = Tag(name=newtag.name)
        self.db.add(tag)
        return tag

    def add_tag_in_post(self, post_id: int, tag_id: int):
        new_tag_post = TagPost(post_id=post_id, tag_id=tag_id)
        self.db.add(new_tag_post)
        return new_tag_post

    async def get_tags(self):
        return (await self.db.execute(select(Tag)
                                     )).scalars().all()

    async def get_tag(self, tag_id: int):
        return (await self.db.execute(select(Tag)
    .where(Tag.id == tag_id))).scalars().first()

    async def get_tag_post(self, post_id: int, tag_id: int):
        return (await self.db.execute(select(TagPost)
        .where(TagPost.post_id==post_id,
        TagPost.tag_id==tag_id)
                 )
        ).scalars().first()

    async def get_post_tags(self, post_id: int):
        return (await self.db.execute(select(TagPost)
        .where(TagPost.post_id == post_id)
        .options(
            *TAGPOST_ROAD_OPTIONS
        )
        )
                ).scalars().all()



    async def delete_post_tags(self, tag_post):
        await self.db.delete(tag_post)
