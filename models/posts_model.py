from app.database import BaseModel
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey
from datetime import datetime

class Post(BaseModel):
    __tablename__ = 'posts'
    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')
    created_at: Mapped[datetime]

    def __repr__(self):
        return f"<id={self.id}, title={self.title}, content={self.content}, user_id={self.user_id}, created_at={self.created_at}>"

from models.user_model import User
from models.comments_model import Comment