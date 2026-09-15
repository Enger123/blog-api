from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# from services.posts import POST_ROAD_OPTIONS, post_returning
from schemas.post import PostResponse, AuthorSchema, PostInfo
from models import Like, Post, User
from schemas.user import UserResponse
from schemas.like import LikeResponse
from repositories import LikeRepository, PostRepository
from services.posts import PostService

class LikeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.like_repository = LikeRepository(db)
        self.post_repository = PostRepository(db)
        self.post_service = PostService(db)

    def likes_returning(self, likes):
        return [LikeResponse(id=l.id,
                             user=AuthorSchema(id=l.user_id,
                                               username=l.user.username
                                               ),
                             post=PostInfo(id=l.post_id,
                                           title=l.post.title)
                             )
                for l in likes]

    async def get_likes_username(self, username: str):
        likes = await self.like_repository.get_likes_username(username)
        if not likes:
            raise HTTPException(status_code=404, detail='Likes not found from this user')
        return self.likes_returning(likes)

    async def add_post_like(self, post_id: int, current_user):
        post = self.post_repository.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        existing_like = await self.like_repository.existed_like(current_user, post_id)
        if existing_like:
            raise HTTPException(status_code=400, detail='You already liked this post')

        like = self.like_repository.add_post_like(current_user, post_id)
        await self.db.commit()
        await self.db.refresh(like)
        await self.db.refresh(post)
        return self.post_service.post_returning(post)

    async def delete_post_like(self, post_id: int, current_user):
        like = await self.like_repository.existed_like(current_user, post_id)
        if not like:
            raise HTTPException(status_code=404, detail='Post not found')
        await self.like_repository.delete_like(like)
        await self.db.commit()
        return {'message': 'Лайк прибрано'}

    async def get_post_id_likes(self, post_id: int):
        post = await self.like_repository.get_post_id_likes(post_id)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        likes = post.likes
        return [UserResponse(id=like.user.id,
                                 username=like.user.username,
                                 created_at=like.user.created_at
                                 ) for like in likes]

    async def get_users_id_likes(self, user_id: int):
        user = await self.like_repository.get_users_id_likes(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return [PostResponse(id = like.post.id,
                                 title=like.post.title,
                                 content=like.post.content,
                                user_id=like.post.user_id,
                                image_path=like.post.image_path,
                                 comments_count=len(like.post.comments),
                                 likes_count=len(like.post.likes),
                                 created_at=like.post.created_at,
                                 user=AuthorSchema(id=user_id,
                                                   username=user.username
                                                   ))
                    for like in user.likes]

