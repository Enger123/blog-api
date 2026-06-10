from fastapi import HTTPException
from app.database import Session
from models import Post
from models.tags_posts_model import TagPost
from models.tags_model import Tag
from schemas.tags import TagResponse, TagCreate
from typing import List
from schemas.tag_post import TagPostResponse

def create_tag(newtag: TagCreate):
    with Session() as session:
        tag = Tag(name=newtag.name)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return TagResponse(id=tag.id,
                           name=tag.name)

def get_tags() -> List[TagResponse]:
    with Session() as session:
        tags = session.query(Tag).all()
        if not tags:
            raise HTTPException(status_code=404, detail='Tags not found')
        return [TagResponse(id=tag.id,
                            name=tag.name) for tag in tags]

def get_post_tags(post_id: int):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        tag_post = session.query(TagPost).filter_by(post_id=post_id).all()
        if not tag_post:
            raise HTTPException(status_code=404, detail='Tags not found')
        return [TagPostResponse(id=t.id,
                            tag_id=t.tag.id,
                            post_id=t.post_id,
                            tag_name=t.tag.name,
                            post_title=t.post.title)
                for t in tag_post]

def add_post_tags(post_id: int, tag_id: int, current_user):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        if post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='You are not the owner of this post')
        tag = session.query(Tag).filter_by(id=tag_id).first()
        if not tag:
            raise HTTPException(status_code=404, detail='Tag not found')
        tag_post = session.query(TagPost).filter_by(post_id=post_id, tag_id=tag_id).first()
        if tag_post:
            raise HTTPException(status_code=400, detail='There is the same tag in this post')
        new_tag_post = TagPost(post_id=post_id, tag_id=tag_id)
        session.add(new_tag_post)
        session.commit()
        session.refresh(new_tag_post)
        return TagPostResponse(id=new_tag_post.id,
                               tag_id=tag_id,
                               post_id=post.id,
                               tag_name=new_tag_post.tag.name,
                               post_title=new_tag_post.post.title
                               )

def delete_post_tags(post_id: int, tag_id: int, current_user) -> dict:
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        if post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='You are not the owner of this post')
        post_tag = session.query(TagPost).filter_by(post_id=post_id, tag_id=tag_id).first()
        if not post_tag:
            raise HTTPException(status_code=404, detail='Tag not found in the post')
        session.delete(post_tag)
        session.commit()
        return {'message': 'Tag deleted in the post'}