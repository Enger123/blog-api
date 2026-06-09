from sqlalchemy import ForeignKey

from app.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tag(BaseModel):
    __tablename__ = 'tags'
    name: Mapped[str]
    tags_posts: Mapped[list['TagPost']] = relationship(back_populates='tag')

    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"

from models.posts_model import Post
from models.tags_posts_model import TagPost