from datetime import datetime

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models.posts_model import Post
from schemas.post import PostCreate
from sqlalchemy.orm import Session
from typing import List
from schemas.post import PostResponse
from models import Tag, TagPost
from models import User

POST_ROAD_OPTIONS = (
    selectinload(Post.user),
    selectinload(Post.comments),
    selectinload(Post.likes)
                     )

USER_ROAD_OPTIONS = (
        selectinload(User.posts)
        .selectinload(Post.comments),

        selectinload(User.posts)
        .selectinload(Post.likes),

        selectinload(User.posts)
        .selectinload(Post.user)
                                )


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_posts_tag(self, tag: str) -> List[PostResponse]:
        posts_query = await self.db.execute(select(Post)
        .join(TagPost)
        .join(Tag)
        .where(Tag.name==tag)
        .options(*POST_ROAD_OPTIONS)
                            )
        return posts_query.scalars().all()

    async def list_posts_settings(self,
                                  query,
                                  skip,
                                  limit
                                  ):
        new_query = await self.db.execute(query
                                  .offset(skip)
                                  .limit(limit)
                                  .options(*POST_ROAD_OPTIONS
                                  )
                                  )
        return new_query.scalars().all()

    async def get_posts_without_setts(self):
        query = await self.db.execute(
            select(Post).options(*POST_ROAD_OPTIONS)
        )
        return query.scalars().all()

    async def get_post(self, post_id: int):
        query = await self.db.execute(
            select(Post).where(Post.id==post_id)
        .options(*POST_ROAD_OPTIONS)
        )
        return query.scalars().first()


    async def get_post_with_userid(self,
                                   current_user,
                                   post_id: int):
        return (await self.db.scalars(select(Post)
                                          .where(Post.id == post_id,
                                                 Post.user_id == current_user.id)
                                          .options(*POST_ROAD_OPTIONS)
                                          )).first()

    async def create_post(self,
                          newpost: PostCreate,
                          current_user
                          ):
        post = Post(title=newpost.title,
                    content=newpost.content,
                    user_id=current_user.id,
                    created_at=datetime.now()
                    )
        self.db.add(post)
        return post

    async def delete_post(self, post):
        await self.db.delete(post)

    async def my_posts(self, current_user) -> List[PostResponse]:
        result = await self.db.execute(select(User)
                                    .where(User.id==current_user.id)
                                .options(
                                    selectinload(User.posts)
                                    .selectinload(Post.comments),

                                    selectinload(User.posts)
                                    .selectinload(Post.likes),

                                    selectinload(User.posts)
                                    .selectinload(Post.user)
                                ))
        return result.scalars().first()

    async def get_posts_username(self, username : str):
        result = await self.db.execute(select(Post)
                                 .join(User)
                                 .where(
            User.username.contains(username)
        )
            .options(
                *POST_ROAD_OPTIONS
            )
        )
        return result.scalars().all()

    async def user_id_posts(self, user_id: int) -> List[PostResponse]:
        user = await (self.db.execute(select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.posts)
            .selectinload(Post.comments),

            selectinload(User.posts)
            .selectinload(Post.likes),

            selectinload(User.posts)
            .selectinload(Post.user)
        )
        )
        )
        return user.scalars().first()

    async def get_post_for_coms(self, post_id: int):
        return (await self.db.execute(select(Post)
                                .where(Post.id==post_id)
                                )).scalars().first()