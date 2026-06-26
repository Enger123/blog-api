from fastapi import HTTPException

from models import TagPost, Post, User, Tag
from schemas.post import PostCreate, PostResponse, PostUpdate, AuthorSchema
from app.database import Session
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

def get_posts_tag(tag: str, db) -> List[PostResponse]:
    posts = db.query(Post)\
    .join(TagPost)\
    .join(Tag)\
    .filter(Tag.name==tag).all()
    post_404(posts)
    return posts_returning(posts)

def add_post(newpost: PostCreate, current_user, db) -> PostResponse:
    post = Post(title=newpost.title,
                content=newpost.content,
                    user_id=current_user.id,
                    created_at=datetime.now()
                    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post_returning(post)

def get_posts(db,
              skip: int = 0,
              limit: int = 10,
              title: str = None,
              sort: str = 'new') -> List[PostResponse]:
    query = db.query(Post)
    if title is not None:
        query = query.filter(Post.title.ilike(f"%{title}%"))
        if sort == 'new':
            query = query.order_by(Post.created_at.desc())
        elif sort == 'old':
            query = query.order_by(Post.created_at)
    posts = query.offset(skip).limit(limit).all()
    return posts_returning(posts)

def get_posts_username(username : str, db) -> List[PostResponse]:
    posts = db.query(Post).join(User).filter(User.username.contains(username)).all()
    if not posts:
        post_404(posts)
    return posts_returning(posts)


def get_post_id(id: int, db) -> PostResponse:
    post = db.query(Post).filter_by(id=id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    return post_returning(post)

def change_post(id: int,
                changed_post: PostUpdate,
                current_user,
                db) -> PostResponse:
    post = db.query(Post).filter_by(id=id, user_id=current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    if changed_post.title is not None:
        post.title = changed_post.title
    if changed_post.content is not None:
        post.content = changed_post.content
    db.commit()
    return post_returning(post)

def delete_post(id: int, current_user, db) -> dict:
    post = db.query(Post).filter_by(id=id, user_id=current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    db.delete(post)
    db.commit()
    return {'message': 'deleted'}

def my_posts(current_user) -> List[PostResponse]:
    with Session() as session:
        our_user = session.query(User).filter_by(id=current_user.id).first()
        posts=our_user.posts
        return posts_returning(posts)

def user_id_posts(user_id: int, db) -> List[PostResponse]:
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    posts = user.posts
    return posts_returning(posts)

def posts_params(pagination, db):
    posts = (db.query(Post)
    .limit(pagination.limit)
    .offset(pagination.offset)
                ).all()
    return posts_returning(posts)