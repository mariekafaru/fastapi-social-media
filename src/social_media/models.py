from sqlalchemy import DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.social_media.database import Base



class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)


class Post(BaseModel):
    __tablename__ = 'posts'
    title: Mapped[str] =mapped_column(nullable= False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False, server_default='TRUE')
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user= relationship('User')


class User(BaseModel):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))


class Vote(BaseModel):
    __tablename__ = 'post_votes'
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'),primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'),primary_key=True, nullable=False)
    post = relationship('Post')
    user = relationship('User')