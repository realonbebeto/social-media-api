from typing import List
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..schemas import CreateUser, GetUser
from ..utils import hashPwd
from .. import models

router = APIRouter(tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GetUser)
async def createUser(user: CreateUser, db: Session = Depends(get_db)):

    # Hash the pssword
    hashed_pwd = hashPwd(user.password)
    user.password = hashed_pwd
    user_q = db.query(models.User).filter_by(email=user.email)

    if user_q.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email} already exists")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=GetUser)
def getUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")

    return user
