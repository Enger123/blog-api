from fastapi import HTTPException
from schemas.post import PostCreate, PostResponse, PostUpdate
from app.database import Session
from models.posts_model import Post
from datetime import datetime
from typing import List

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
        return PostResponse(id=post.id,
                            title=post.title,
                            content=post.content,
                            created_at=post.created_at,
                            author={'id': post.user.id,
                                    'username': post.user.username
                                    }
                            )

def get_posts() -> List[PostResponse]:
    with Session() as session:
        posts = session.query(Post).all()
        return [PostResponse.model_validate(post) for post in posts]

def get_post_id(id: int) -> PostResponse:
    with Session() as session:
        post = session.query(Post).filter_by(id=id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        return PostResponse.model_validate(post)

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
        return PostResponse.model_validate(post)

def delete_post(id: int, current_user) -> dict:
    with Session() as session:
        post = session.query(Post).filter_by(id=id, user_id=current_user.id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        session.delete(post)
        session.commit()
        return {'message': 'deleted'}