from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import UserLogin, Token
from ..utils import verify
from ..oauth2 import createAccessToken


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=Token)
def signIn(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = createAccessToken(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    # create token
    # return token
