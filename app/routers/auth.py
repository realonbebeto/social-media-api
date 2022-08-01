from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import UserLogin
from ..utils import verify

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def signIn(user_cred: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_cred.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    return {"data": "successfully authenticated"}
    # create token
    # return token
