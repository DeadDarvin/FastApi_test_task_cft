from datetime import datetime
from datetime import timedelta

from jose import jwt

import constans


def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=constans.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, constans.SECRET_KEY, constans.ALGORITHM)

    return encoded_jwt
