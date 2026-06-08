from sqlalchemy import ForeignKey
from app.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Like(BaseModel):
    __tablename__ = "likes"
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship(back_populates='likes')
    user: Mapped['User'] = relationship(back_populates='likes')

    def __repr__(self):
        return f"<id={self.id}, user_id={self.user_id}, post_id={self.post_id}>"

from models.posts_model import Post
from models.user_model import User