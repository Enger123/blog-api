from fastapi import HTTPException
from app.database import Session
from models import Post, TagPost, User, Tag, Like
from schemas.tags import TagResponse, TagCreate
from typing import List
from schemas.tag_post import TagPostResponse
from crud.posts import post_404

def tag_post_404(tag_post):
    if not tag_post:
        raise HTTPException(status_code=404, detail='Tags not found')

def get_tags_postliked(username: str, db) -> List[TagResponse]:
    tags = db.query(Tag)\
        .join(TagPost)\
        .join(Post)\
        .join(Like)\
        .join(User)\
        .filter(User.username==username).all()
    if not tags:
            raise HTTPException(status_code=404,
                                detail=f'Tags not found in the posts liked by {username}')
    return [TagResponse(id=tag.id, name=tag.name) for tag in tags]

def get_tags_inpost_username(username: str, db) -> List[TagResponse]:
    tags = db.query(Tag)\
            .join(TagPost)\
            .join(Post)\
            .join(User)\
            .filter(User.username.contains(username)).all()
    return [TagResponse(id=tag.id,
                            name=tag.name) for tag in tags]

def create_tag(newtag: TagCreate, db):
    tag = Tag(name=newtag.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagResponse(id=tag.id,
                           name=tag.name)

def get_tags(db) -> List[TagResponse]:
    tags = db.query(Tag).all()
    print(tags)
    if not tags:
        raise HTTPException(status_code=404, detail='Tags not found')
    return [TagResponse(id=tag.id,
                            name=tag.name) for tag in tags]

def get_post_tags(post_id: int, db):
    post = db.query(Post).filter_by(id=post_id).first()
    post_404(post)
    tag_post = db.query(TagPost).filter_by(post_id=post_id).all()
    tag_post_404(tag_post)
    return [TagPostResponse(id=t.id,
                            tag_id=t.tag.id,
                            post_id=t.post_id,
                            tag_name=t.tag.name,
                            post_title=t.post.title)
                for t in tag_post]

def add_post_tags(post_id: int, tag_id: int, current_user, db):
    post = db.query(Post).filter_by(id=post_id).first()
    post_404(post)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='You are not the owner of this post')
    tag = db.query(Tag).filter_by(id=tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')
    tag_post = db.query(TagPost).filter_by(post_id=post_id, tag_id=tag_id).first()
    if tag_post:
        raise HTTPException(status_code=400, detail='There is the same tag in this post')
    new_tag_post = TagPost(post_id=post_id, tag_id=tag_id)
    db.add(new_tag_post)
    db.commit()
    db.refresh(new_tag_post)
    return TagPostResponse(id=new_tag_post.id,
                               tag_id=tag_id,
                               post_id=post.id,
                               tag_name=new_tag_post.tag.name,
                               post_title=new_tag_post.post.title
                               )

def delete_post_tags(post_id: int, tag_id: int, current_user, db) -> dict:
    post = db.query(Post).filter_by(id=post_id).first()
    post_404(post)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='You are not the owner of this post')
    tag_post = db.query(TagPost).filter_by(post_id=post_id, tag_id=tag_id).first()
    tag_post_404(tag_post)
    db.delete(tag_post)
    db.commit()
    return {'message': 'Tag deleted in the post'}