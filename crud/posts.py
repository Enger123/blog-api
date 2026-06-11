from fastapi import HTTPException
from schemas.post import PostCreate, PostResponse, PostUpdate, AuthorSchema
from app.database import Session
from models.posts_model import Post
from models.user_model import User
from datetime import datetime
from typing import List

def post_404(post):
    if not post:
        raise HTTPException(status_code=404, detail='Post/posts not found')

def post_returning(post):
    return PostResponse(id=post.id,
                        title=post.title,
                        content=post.content,
                        comments_count=len(post.comments),
                        likes_count=len(post.likes),
                        created_at=post.created_at,
                        user=AuthorSchema(id=post.user.id,
                                          username=post.user.username
                                          )
                        )

def posts_returning(posts):
    return [PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        comments_count=len(post.comments),
        likes_count=len(post.likes),
        created_at=post.created_at,
        user=AuthorSchema(id=post.user.id,
                          username=post.user.username)
    ) for post in posts
    ]


def add_post(newpost: PostCreate, current_user) -> PostResponse:
    with Session() as session:
        post = Post(title=newpost.title,
                    content=newpost.content,
                    user_id=current_user.id,
                    created_at=datetime.now()
                    )
        session.add(post)
        session.commit()
        session.refresh(post)
        return post_returning(post)

def get_posts(skip: int = 0, limit: int = 10, title: str = None, sort: str = 'new') -> List[PostResponse]:
    with Session() as session:
        query = session.query(Post)
        if title is not None:
            query = query.filter(Post.title.ilike(f"%{title}%"))
        if sort == 'new':
            query = query.order_by(Post.created_at.desc())
        elif sort == 'old':
            query = query.order_by(Post.created_at)
        posts = query.offset(skip).limit(limit).all()
        return posts_returning(posts)

def get_posts_username(username : str) -> List[PostResponse]:
    with Session() as session:
        posts = session.query(Post).join(User).filter(User.username.contains(username)).all()
        if not posts:
            post_404(posts)
        return posts_returning(posts)


def get_post_id(id: int) -> PostResponse:
    with Session() as session:
        post = session.query(Post).filter_by(id=id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        return post_returning(post)

def change_post(id: int, changed_post: PostUpdate, current_user) -> PostResponse:
    with Session() as session:
        post = session.query(Post).filter_by(id=id, user_id=current_user.id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        if changed_post.title is not None:
            post.title = changed_post.title
        if changed_post.content is not None:
            post.content = changed_post.content
        session.commit()
        return post_returning(post)

def delete_post(id: int, current_user) -> dict:
    with Session() as session:
        post = session.query(Post).filter_by(id=id, user_id=current_user.id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        session.delete(post)
        session.commit()
        return {'message': 'deleted'}

def my_posts(current_user) -> List[PostResponse]:
    with Session() as session:
        our_user = session.query(User).filter_by(id=current_user.id).first()
        posts=our_user.posts
        return posts_returning(posts)

def user_id_posts(user_id: int) -> List[PostResponse]:
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        posts = user.posts
        return posts_returning(posts)