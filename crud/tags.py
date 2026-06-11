from fastapi import HTTPException
from app.database import Session
from models import Post, TagPost, User
from schemas.tags import TagResponse, TagCreate
from typing import List
from schemas.tag_post import TagPostResponse
from crud.posts import post_404

def tag_post_404(tag_post):
    if not tag_post:
        raise HTTPException(status_code=404, detail='Tags not found')

def get_tags_inpost_username(username: str) -> List[TagResponse]:
    with Session() as session:
        tags = session.query(TagPost).join(User).filter(User.username.contains(username))
        print(tags)
        tag_post_404(tags)
        return [TagResponse(id=tag.id,
                            name=tag.name) for tag in tags]

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
        post_404(post)
        tag_post = session.query(TagPost).filter_by(post_id=post_id).all()
        tag_post_404(tag_post)
        return [TagPostResponse(id=t.id,
                            tag_id=t.tag.id,
                            post_id=t.post_id,
                            tag_name=t.tag.name,
                            post_title=t.post.title)
                for t in tag_post]

def add_post_tags(post_id: int, tag_id: int, current_user):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        post_404(post)
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
        post_404(post)
        if post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='You are not the owner of this post')
        tag_post = session.query(TagPost).filter_by(post_id=post_id, tag_id=tag_id).first()
        tag_post_404(tag_post)
        session.delete(tag_post)
        session.commit()
        return {'message': 'Tag deleted in the post'}