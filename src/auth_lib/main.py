import base64
import datetime
import os
from typing import Dict
from uuid import UUID
from fastapi import HTTPException, Request
import jwt
from passlib.hash import bcrypt
from fastapi import status

from src.db import get_db

TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def generate_salt() -> str:
    return base64.b64encode(os.urandom(16)).decode('utf-8')


def hash_password(password: str) -> str:
    return bcrypt.hash(password.encode())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def generate_token(sub: UUID, **body):
    expire = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(sub),
        **body,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Dict:
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

        # Check for expiration (if 'exp' is present)
        if datetime.datetime.now(datetime.timezone.utc) > datetime.datetime.fromtimestamp(payload["exp"]).replace(tzinfo=datetime.timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

        # Return the payload (user data, etc.) from the decoded token
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = verify_token(token)

    return user
