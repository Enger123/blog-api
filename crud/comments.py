from fastapi import HTTPException
from datetime import datetime
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from typing import List
from schemas.post import AuthorSchema, PostInfo
from models import Comment, Post, User
from sqlalchemy import select
from sqlalchemy.orm import selectinload, defer

async def get_comments_with_relations(comment_id: int, db, current_user):
    comment_query = await db.execute(select(Comment)
    .where(Comment.id == comment_id #для тесту без current_user (403 код помилки)
           )
    .options(
        selectinload(Comment.post),
        selectinload(Comment.user)
    )
    )
    return comment_query.scalars().first()

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

def coms_returning(comments):
    return [CommentResponse(id=c.id,
                            text=c.text,
                            user=AuthorSchema(id=c.user.id,
                                                username=c.user.username),
                            post=PostInfo(id=c.post.id,
                                            title=c.post.title),
                            created_at=c.created_at)
            for c in comments]

async def get_comments_username(username: str, db) -> List[CommentResponse]:
    db_query = await db.execute(select(Comment)
    .join(User)
    .where(User.username.contains(username))
    .options(
        selectinload(Comment.post),
        selectinload(Comment.user)
    )
           )
    comments = db_query.scalars().all()
    if not comments:
        raise HTTPException(status_code=404, detail='Comments not found from this user')
    return coms_returning(comments)

async def add_post_comment(id: int, newcomment: CommentCreate, current_user, db) -> CommentResponse:
    post_query = await db.execute(select(Post)
                            .where(Post.id==id)
                            )
    post = post_query.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    comment = Comment(text=newcomment.text,
                          user_id=current_user.id,
                          post_id=post.id,
                          created_at=datetime.now()
    )
    db.add(comment)
    await db.commit()
    com_query = await db.execute(select(Comment)
                                   .options(
        selectinload(Comment.user),
        selectinload(Comment.post)
    )
                                   )
    com = com_query.scalars().first()
    return com_returning(com)

async def get_post_comments(post_id: int, db) -> List[CommentResponse]:
    post_query = await db.execute(select(Post)
                            .where(Post.id==post_id)
                                  .options(
        selectinload(Post.comments).selectinload(Comment.post),
        selectinload(Post.comments).selectinload(Comment.user)
                                           )
                                  )
    post = post_query.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    comments = post.comments
    return coms_returning(comments)

async def delete_com(comment_id: int, current_user, db):
    comment_query = await db.execute(select(Comment)
                               .where(Comment.id==comment_id,
                                      Comment.user_id==current_user.id)
                                     )
    comment = comment_query.scalars().first()
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    await db.delete(comment)
    await db.commit()
    return {'message': 'Comment deleted'}

async def change_com(comment_id: int, com: CommentUpdate, current_user, db):
    comment = await get_comments_with_relations(comment_id, db, current_user)
    if comment.user_id != current_user.id: #для тесту ця перевірка (403 код помилки)
        raise HTTPException(
            status_code=403,
            detail='You can not change this comment')
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    if com.text is not None:
        comment.text = com.text
    await db.commit()
    comment = await get_comments_with_relations(comment_id, db, current_user)
    return com_returning(comment)