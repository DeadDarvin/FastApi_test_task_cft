from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt
from jose import JWTError

import constans


def create_access_token(username: str, expire: datetime = None) -> str:
    if not expire:
        expire = datetime.utcnow() + timedelta(
            minutes=constans.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, constans.SECRET_KEY, constans.ALGORITHM)

    return encoded_jwt


def get_email_from_jwt(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, constans.SECRET_KEY, constans.ALGORITHM)
        email = payload.get("sub")
    except JWTError:
        return

    return email
