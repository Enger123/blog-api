from fastapi import HTTPException
from datetime import datetime
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from typing import List
from app.database import Session
from models.comments_model import Comment, Post

def add_post_comment(id: int, newcomment: CommentCreate, current_user) -> CommentResponse:
    with Session() as session:
        post = session.query(Post).filter_by(id=id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        comment = Comment(text=newcomment.text,
                          user_id=current_user.id,
                          post=post,
                          created_at=datetime.now()
        )
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return CommentResponse.model_validate(comment)

def get_post_comments(post_id: int) -> List[CommentResponse]:
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        comments = post.comments
        return [CommentResponse.model_validate(comment) for comment in comments]

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
        return CommentResponse.model_validate(comment)