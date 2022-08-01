
from typing import Text
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from datetime import datetime


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.now())
