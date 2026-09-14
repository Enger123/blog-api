from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import CommentRepository, PostRepository
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from typing import List
from schemas.post import AuthorSchema, PostInfo
from models import Comment
from sqlalchemy import select
from sqlalchemy.orm import selectinload, defer

class CommentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.comment_repository = CommentRepository(db)
        self.post_repository = PostRepository(db)

    async def get_comments_with_relations(self, comment_id: int, current_user):
        return await self.comment_repository.get_comments_with_relations(
            comment_id, current_user
        )

    def com_returning(self, comment):
        return CommentResponse(
            id=comment.id,
            text=comment.text,
            user=AuthorSchema(
                id=comment.user.id,
                username=comment.user.username
            ),
            post=PostInfo(
                id=comment.post.id,
                title=comment.post.title
            ),
            created_at=comment.created_at
        )

    def coms_returning(self, comments):
        return [CommentResponse(id=c.id,
                                text=c.text,
                                user=AuthorSchema(id=c.user.id,
                                                    username=c.user.username),
                                post=PostInfo(id=c.post.id,
                                                title=c.post.title),
                                created_at=c.created_at)
                for c in comments]

    async def get_comments_username(self, username: str) -> List[CommentResponse]:
        comments = await self.comment_repository.get_comments_username(username)
        if not comments:
            raise HTTPException(status_code=404, detail='Comments not found from this user')
        return self.coms_returning(comments)

    async def add_post_comment(self,
                               id: int,
                               newcomment: CommentCreate,
                               current_user) -> CommentResponse:
        post = await self.post_repository.get_post_for_coms(id)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        comment = self.comment_repository.create_com_for_post(
            newcomment, post, current_user
        )
        await self.db.commit()
        await self.db.refresh(comment)
        print(comment)
        com = await self.comment_repository.get_comment_with_options()
        return self.com_returning(com)

    async def get_post_comments(self, post_id: int) -> List[CommentResponse]:
        post = await self.comment_repository.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        comments = post.comments
        return self.coms_returning(comments)

    async def delete_com(self, comment_id: int, current_user):
        comment = await self.comment_repository.get_user_com(comment_id, current_user)
        if not comment:
            raise HTTPException(status_code=404, detail='Comment not found')
        await self.comment_repository.delete_com(comment)
        await self.db.commit()
        return {'message': 'Comment deleted'}

    async def change_com(self, comment_id: int, com: CommentUpdate, current_user):
        comment = await self.get_comments_with_relations(comment_id, current_user)
        # if comment.user_id != current_user.id: #для тесту ця перевірка (403 код помилки)
        #     raise HTTPException(
        #         status_code=403, ЦЯ ПЕРЕВІРКА НЕ ВІРНА, БО NONETYPE ПОВЕРНЕТЬСЯ
        #         detail='You can not change this comment')
        if not comment:
            raise HTTPException(status_code=404, detail='Comment not found')
        if com.text is not None:
            comment.text = com.text
        await self.db.commit()
        comment = await self.get_comments_with_relations(comment_id, current_user)
        return self.com_returning(comment)