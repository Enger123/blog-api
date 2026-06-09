from fastapi import HTTPException

from app.database import Session
from models import Post
from models.tags_posts_model import TagPost
from models.tags_model import Tag
from schemas.tags import TagResponse, TagCreate


def get_post_tags(post_id: int):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        tags = post.tags_posts.tag
        print(tags)
        if not tags:
            raise HTTPException(status_code=404, detail='Tags not found for this post')
        return [TagResponse(id=tag.id,
                            name=tag.name,
                            post_id=post_id)
                for tag in tags]

def add_post_tags(post_id: int, newtag: TagCreate):
    with Session() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')
        tag = Tag(name=newtag.name)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return TagResponse(id=tag.id,
                           name=tag.name,
                           post_id=post_id)