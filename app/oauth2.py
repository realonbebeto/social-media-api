from jose import JWSError, jwt
from datetime import datetime, timedelta, timezone

SECRECTE_KEY = "!A%D*G-KaPdSgVkXp2s5v8y/B?E(H+MbQeThWmZq3t6w9z$C&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdSgVkYp3s6v9y/B?E(H+MbQeThWmZq4t7w!z%C&F)J@NcRfUjXn"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2


def createAccessToken(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    encoded = jwt.encode(payload, SECRECTE_KEY, algorithm=ALGORITHM)

    return encoded
