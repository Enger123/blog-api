from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import Like, User, Post
from sqlalchemy import select

LIKES_ROAD_OPTIONS = (
    selectinload(Like.user),
    selectinload(Like.post)

)

class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_likes_username(self, username: str):
        return (await self.db.execute(select(Like)
                                 .join(User)
                                 .where(User.username.contains(username))
                                 .options(*LIKES_ROAD_OPTIONS)
                                       )
                ).scalars().all()

    def add_post_like(self, current_user, post_id: int):
        like = Like(user_id=current_user.id, post_id=post_id)
        self.db.add(like)
        return like

    async def existed_like(self, current_user, post_id: int):
        return (await self.db.execute(select(Like)
                .where(Like.user_id==current_user.id,
                       Like.post_id==post_id)
                                 )
                ).scalars().first()

    async def get_post_id_likes(self, post_id: int):
        return (await self.db.execute(select(Post)
                    .where(Post.id == post_id)
                    .options(selectinload(Post.likes).selectinload(Like.user))
            )).scalars().first()

    async def get_users_id_likes(self, user_id: int):
        return (await self.db.execute(select(User)
                                      .where(User.id == user_id)
                                      .options(selectinload(User.likes)
                                               .selectinload(Like.post)
                                               .selectinload(Post.likes),
                                               selectinload(User.likes)
                                               .selectinload(Like.post)
                                               .selectinload(Post.comments)
                                               )
                                      )
                ).scalars().first()

    async def delete_like(self, like):
        await self.db.delete(like)
