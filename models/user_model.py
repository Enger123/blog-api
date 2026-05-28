from app.database import BaseModel
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime

class User(BaseModel):
    __tablename__ = 'users'
    username: Mapped[str]
    hashed_password: Mapped[str]
    created_at: Mapped[datetime]
    posts: Mapped[list['Post']] = relationship(back_populates='user')
    comments: Mapped[list['Comment']] = relationship(back_populates='user')

    def __repr__(self):
        return f"<id={self.id}, username={self.username}, hashed_password={self.hashed_password}, created_at={self.created_at}>"


from models.posts_model import Post
from models.comments_model import Comment