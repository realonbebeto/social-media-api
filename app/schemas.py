from pydantic import BaseModel, EmailStr
from typing import *
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class GetPost(PostResponse):
    pass


class UserBase(BaseModel):
    email: EmailStr


class CreateUser(UserBase):
    password: str
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class GetUser(UserResponse):
    pass


class UpdateUser(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    pass


class UserLogin(UserBase):
    password: str
