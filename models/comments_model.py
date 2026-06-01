from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey

class Comment(BaseModel):
    __tablename__ = 'comments'
    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    user: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')
    created_at: Mapped[datetime]

    def __repr__(self):
        return f"<id={self.id}, text={self.text}, user_id={self.user_id}, post_id={self.post_id}, created_at={self.created_at}>"

from models.user_model import User
from models.posts_model import Post
