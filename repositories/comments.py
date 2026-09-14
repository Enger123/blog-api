from sqlalchemy.ext.asyncio import AsyncSession
from models import Post, Comment, User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from schemas.comment import CommentCreate


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_comments_username(self, username: str):
        return (await self.db.scalars(select(Comment)
        .join(User)
        .where(User.username.contains(username))
        .options(
            selectinload(Comment.post),
            selectinload(Comment.user)
        )
               )
                ).all()

    async def get_post(self, post_id: int):
        return (await self.db.execute(select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.comments).selectinload(Comment.post),
            selectinload(Post.comments).selectinload(Comment.user)
        )
        )).scalars().first()

    async def get_user_com(self, comment_id, current_user):
        return (await self.db.execute(select(Comment)
                   .where(Comment.id==comment_id,
                   Comment.user_id==current_user.id)
                )).scalars().first()

    async def get_comment_with_options(self):
        return (await self.db.execute(select(Comment)
                                       .options(
            selectinload(Comment.user),
            selectinload(Comment.post)
        )
                                       )).scalars().first()

    async def get_comments_with_relations(self, comment_id: int, current_user):
        return (await self.db.execute(select(Comment)
        .where(Comment.id == comment_id, Comment.user_id == current_user.id
               )
        .options(
            selectinload(Comment.post),
            selectinload(Comment.user)
        )
        )).scalars().first()


    def create_com_for_post(self,
                                  newcomment: CommentCreate,
                                  post,
                                  current_user):
        comment = Comment(text=newcomment.text,
                          user_id=current_user.id,
                          post_id=post.id,
                          created_at=datetime.now()
                          )
        self.db.add(comment)
        return comment

    async def delete_com(self, comment):
        await self.db.delete(comment)