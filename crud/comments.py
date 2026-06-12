from fastapi import HTTPException
from datetime import datetime
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from typing import List
from app.database import Session
from schemas.post import AuthorSchema, PostInfo
from models import Comment, Post, User

def com_returning(comment):
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

def get_comments_username(username: str) -> List[CommentResponse]:
    with Session() as session:
        comments = session.query(Comment)\
        .join(Post)\
        .join(User)\
        .filter(User.username.contains(username)).all()
        if not comments:
            raise HTTPException(status_code=404, detail='Comments not found from this user')
        return [CommentResponse(id=c.id,
                                text=c.text,
                                user=AuthorSchema(id=c.user.id,
                                                  username=c.user.username),
                                post=PostInfo(id=c.post.id,
                                              title=c.post.title),
                                created_at=c.created_at)
                for c in comments]

def add_post_comment(id: int, newcomment: CommentCreate, current_user) -> CommentResponse:
    with Session() as session:
        post = session.query(Post).filter_by(id=id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        comment = Comment(text=newcomment.text,
                          user_id=current_user.id,
                          post_id=post.id,
                          created_at=datetime.now()
        )
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return com_returning(comment)

def get_post_comments(post_id: int) -> List[CommentResponse]:
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        comments = post.comments
        return [CommentResponse(id=comment.id,
            text=comment.text,
            user=AuthorSchema(
                id=comment.user.id,
                username=comment.user.username
            ),
            post=PostInfo(
                id=post_id,
                title=post.title
            ),
            created_at=comment.created_at
                                )
                for comment in comments]

def delete_com(comment_id: int, current_user):
    with Session() as session:
        comment = session.query(Comment).filter_by(id=comment_id, user_id=current_user.id).first()
        if not comment:
            raise HTTPException(status_code=404, detail='Comment not found')
        session.delete(comment)
        session.commit()
        return {'message': 'Comment deleted'}

def change_com(comment_id: int, com: CommentUpdate, current_user):
    with Session() as session:
        comment = session.query(Comment).filter_by(id=comment_id, user_id=current_user.id).first()
        if not comment:
            raise HTTPException(status_code=404, detail='Comment not found')
        if com.text is not None:
            comment.text = com.text
        session.commit()
        return com_returning(comment)