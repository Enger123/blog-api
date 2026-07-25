from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from models import Post, TagPost, User, Tag, Like
from schemas.tags import TagResponse, TagCreate
from typing import List
from schemas.tag_post import TagPostResponse
from crud.posts import post_404
from sqlalchemy import select

TAGPOST_ROAD_OPTIONS = (
    selectinload(TagPost.post),
    selectinload(TagPost.tag)
)

def tag_post_404(tag_post):
    if not tag_post:
        raise HTTPException(status_code=404, detail='Tags not found')

async def get_tags_postliked(username: str, db) -> List[TagResponse]:
    tags_query = await db.execute(select(Tag)
        .join(TagPost)\
        .join(Post)\
        .join(Like)\
        .join(User)\
        .where(User.username==username))
    tags = tags_query.scalars().all()
    if not tags:
            raise HTTPException(status_code=404,
                                detail=f'Tags not found in the posts liked by {username}')
    return [TagResponse(id=tag.id, name=tag.name) for tag in tags]

async def get_tags_inpost_username(username: str, db) -> List[TagResponse]:
    tags_query = await db.execute(select(Tag)
            .join(TagPost)
            .join(Post)
            .join(User)
            .where(User.username.contains(username)))
    tags = tags_query.scalars().all()
    return [TagResponse(id=tag.id,
                            name=tag.name) for tag in tags]

async def create_tag(newtag: TagCreate, db):
    tag = Tag(name=newtag.name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return TagResponse(id=tag.id,
                           name=tag.name)

async def get_tags(db) -> List[TagResponse]:
    tags_query = await db.execute(select(Tag))
    tags = tags_query.scalars().all()
    if not tags:
        raise HTTPException(status_code=404, detail='Tags not found')
    return [TagResponse(id=tag.id,
                            name=tag.name) for tag in tags]

async def get_post_tags(post_id: int, db):
    post_query = await db.execute(select(Post)
                            .where(Post.id==post_id))
    post = post_query.scalars().first()
    post_404(post)
    tag_post_query = await db.execute(select(TagPost)
                                .where(TagPost.post_id==post_id)
                                .options(
        *TAGPOST_ROAD_OPTIONS
    )
                                      )
    tag_post = tag_post_query.scalars().all()
    tag_post_404(tag_post)
    return [TagPostResponse(id=t.id,
                            tag_id=t.tag.id,
                            post_id=t.post_id,
                            tag_name=t.tag.name,
                            post_title=t.post.title)
                for t in tag_post]

async def add_post_tags(post_id: int, tag_id: int, current_user, db):
    post_query = await db.execute(select(Post)
                            .where(Post.id==post_id)
                            )
    post = post_query.scalars().first()
    post_404(post)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='You are not the owner of this post')
    tag_query = await db.execute(select(Tag)
                           .where(Tag.id==tag_id))
    tag = tag_query.scalars().first()
    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')
    tag_post_query = await db.execute(select(TagPost)
                                .where(TagPost.post_id==post_id,
                                       TagPost.tag_id==tag_id)
                                )
    tag_post = tag_post_query.scalars().first()
    if tag_post:
        raise HTTPException(status_code=400, detail='There is the same tag in this post')
    new_tag_post = TagPost(post_id=post_id, tag_id=tag_id)
    db.add(new_tag_post)
    await db.commit()
    await db.refresh(tag)
    await db.refresh(post)
    await db.refresh(new_tag_post)
    return TagPostResponse(id=new_tag_post.id,
                               tag_id=tag.id,
                               post_id=post.id,
                               tag_name=tag.name,
                               post_title=post.title
                               )

async def delete_post_tags(post_id: int, tag_id: int, current_user, db) -> dict:
    post_query = await db.execute(select(Post)
                            .where(Post.id==post_id))
    post = post_query.scalars().first()
    post_404(post)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='You are not the owner of this post')
    tag_post_query = await db.execute(select(TagPost)
                                .where(TagPost.post_id==post_id,
                                       TagPost.tag_id==tag_id))
    tag_post = tag_post_query.scalars().first()
    tag_post_404(tag_post)
    await db.delete(tag_post)
    await db.commit()
    return {'message': 'Tag deleted in the post'}