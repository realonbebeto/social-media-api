from os import access
from pydantic import BaseModel, EmailStr, validator
from typing import *
from datetime import datetime


class EmailResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    phone_number: str


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
    #owner_id: int
    owner: EmailResponse

    class Config:
        orm_mode = True


class GetPost(BaseModel):
    Post: PostResponse
    likes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class LikeBase(BaseModel):
    post_id: int
    direction: int


class CreateLike(LikeBase):
    @validator('direction')
    def zeroOrOne(cls, v):
        if v > 1 or v < 0:
            raise ValueError(
                'Invalid value: Direction must be one(1) or zero(0)')
        return v
    pass
