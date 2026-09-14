from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user
# from cache.redis_caching import RedisCached
from models import TagPost, Post, User, Tag
from repositories.posts import PostRepository
from schemas.post import PostCreate, PostResponse, PostUpdate, AuthorSchema
from datetime import datetime
from typing import List
from exceptions.errors import PostNotFound
from pathlib import Path
import aiofiles
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session


project_dir = Path(__file__).parent.parent
uploads_dir = project_dir / 'uploads'
uploads_dir.mkdir(exist_ok=True)
posts_dir = uploads_dir / 'posts'
posts_dir.mkdir(exist_ok=True)


def post_404(post):
    if not post:
        raise HTTPException(status_code=404, detail='Post/posts not found')

class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.post_repository = PostRepository(db)

    def post_returning(self, post):
        return PostResponse(id=post.id,
                            title=post.title,
                            content=post.content,
                            user_id=post.user_id,
                            image_path=post.image_path,
                            comments_count=len(post.comments),
                            likes_count=len(post.likes),
                            created_at=post.created_at,
                            user=AuthorSchema(id=post.user.id,
                                              username=post.user.username
                                              )
                            )

    def posts_returning(self, posts):
        return [PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            user_id=post.user_id,
            image_path=post.image_path,
            comments_count=len(post.comments),
            likes_count=len(post.likes),
            created_at=post.created_at,
            user=AuthorSchema(id=post.user.id,
                              username=post.user.username)
        ) for post in posts
        ]

    async def get_posts_tag(self, tag: str) -> List[PostResponse]:
        posts = await self.post_repository.get_posts_tag(tag)
        post_404(posts)
        return self.posts_returning(posts)

    async def add_post(self, newpost: PostCreate, current_user) -> PostResponse:
        new_post = await self.post_repository.create_post(newpost, current_user)
        await self.db.commit()
        await self.db.refresh(new_post)
        post_to_return = await self.post_repository.get_post_with_opt(new_post.id)

        return self.post_returning(post_to_return)

    async def add_post_image(self, id: int, current_user, file: UploadFile):
        path = Path(file.filename)
        stem = path.stem
        suffix = path.suffix.lower()
        file_size = len(await file.read())
        existing_post = await self.post_repository.get_post_with_userid(current_user, id)
        if not existing_post:
            raise HTTPException(status_code=404, detail='Post not found')
        if suffix not in ['.jpg', '.png', '.jpeg', '.webp']:
            raise HTTPException(status_code=400,
                                detail=f'You can not upload a \"{suffix}\" file')
        if file_size > 3000000:
            raise HTTPException(status_code=400,
                                detail="Size of a given file can not be more that 3 mB")
        if existing_post.image_path is not None:
            old_file = Path(existing_post.image_path)
            if old_file.exists():
                old_file.unlink()
        loc = posts_dir / file.filename
        i = 1
        while loc.exists():
            new_filename = f"{stem}({i}){suffix}"
            loc = posts_dir / new_filename
            i += 1
        existing_post.image_path = str(loc)
        await file.seek(0)
        content = await file.read()
        with open(loc, 'wb') as f:
            f.write(content)
        await self.db.commit()
        existing_post = await self.post_repository.get_post_with_userid(current_user, id)
        return self.post_returning(existing_post)

    async def delete_post_image(self, id: int,
                                current_user):
        post = await self.post_repository.get_post_with_userid(current_user, id)
        if not post:
            raise PostNotFound
        if post.image_path is not None:
            file_to_del = Path(post.image_path)
            if file_to_del.exists():
                file_to_del.unlink()
            post.image_path = None
            await self.db.commit()
        else:
            raise HTTPException(status_code=400,
                                detail='This post does not have an image')
        return {'message': 'Image deleted'}

    async def get_posts_without_settings(self):
        posts = await self.post_repository.get_posts_without_setts()
        return self.posts_returning(posts)

    async def get_posts(self,
                  skip: int = 0,
                  limit: int = 10,
                  title: str = None,
                  sort: str = 'new') -> List[PostResponse]:
        query = select(Post)
        if title is not None:
            query = query.where(Post.title.ilike(f"%{title}%"))
            if sort == 'new':
                query = query.order_by(Post.created_at.desc())
            elif sort == 'old':
                query = query.order_by(Post.created_at)
        posts = await self.post_repository.list_posts_settings(query, skip, limit)
        return self.posts_returning(posts)

    async def get_posts_username(self, username : str) -> List[PostResponse]:
        posts = await self.post_repository.get_posts_username(username)
        if not posts:
            post_404(posts)
        return self.posts_returning(posts)

    async def get_post_id(self, id: int) -> PostResponse:
        post = await self.post_repository.get_post_with_opt(id)
        if not post:
            raise PostNotFound
        return self.post_returning(post)

    async def change_post(self, id: int,
                    changed_post: PostUpdate,
                    current_user) -> PostResponse:
        checked_post = await self.post_repository.get_post_with_userid(current_user, id)
        if not checked_post:
            raise HTTPException(status_code=404, detail='Post not found')
        if changed_post.title is not None:
            checked_post.title = changed_post.title
        if changed_post.content is not None:
            checked_post.content = changed_post.content
        await self.db.commit()
        await self.db.refresh(checked_post)
        return self.post_returning(checked_post)

    async def delete_post(self, id: int, current_user) -> dict:
        post = await self.post_repository.get_post_with_userid(current_user, id)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        if post.image_path is not None:
            file_to_del = Path(post.image_path)
            if file_to_del.exists():
                file_to_del.unlink()
        await self.post_repository.delete_post(post)
        await self.db.commit()
        return {'message': 'deleted'}

    async def my_posts(self, current_user) -> List[PostResponse]:
        user = await self.post_repository.my_posts(current_user)
        posts = user.posts
        return self.posts_returning(posts)

    async def user_id_posts(self, user_id: int) -> List[PostResponse]:
        user = await self.post_repository.user_id_posts(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        posts = user.posts
        return self.posts_returning(posts)

    async def posts_params(self, pagination):
        db_query = select(Post)
        posts = await self.post_repository.list_posts_settings(
            db_query, pagination.offset, pagination.limit
        )
        return self.posts_returning(posts)