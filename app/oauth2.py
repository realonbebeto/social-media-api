from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from .schemas import TokenData
from .database import get_db
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRECT_KEY = "!A%D*G-KaPdSgVkXp2s5v8y/B?E(H+MbQeThWmZq3t6w9z$C&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdSgVkYp3s6v9y/B?E(H+MbQeThWmZq4t7w!z%C&F)J@NcRfUjXn"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def createAccessToken(data: dict):
    payload = data.copy()
    # datetime.utcnow()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    encoded = jwt.encode(payload, SECRECT_KEY, algorithm=ALGORITHM)

    return encoded


def verifyAccessToken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except JWSError:
        raise credentials_exception

    return token_data


def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not valid credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToken(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
