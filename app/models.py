from venv import create
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, update
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy_utils import EmailType
from datetime import datetime, timezone


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.now(timezone.utc))


class Like(Base):

    __tablename__ = 'likes'

    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        onupdate=datetime.now(timezone.utc))
