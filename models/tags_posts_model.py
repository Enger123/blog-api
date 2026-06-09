from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import BaseModel


class TagPost(BaseModel):
    __tablename__ = 'tags_posts'

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'))
    post: Mapped['Post'] = relationship(back_populates='tags_posts')
    tag: Mapped['Tag'] = relationship(back_populates='tags_posts')
    def __repr__(self):
        return f"<id={self.id}, post_id={self.post_id}, tag_id={self.tag_id}>"

from models.posts_model import Post
from models.tags_model import Tag