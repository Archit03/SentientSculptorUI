from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends
from apps.web.models.users import Users
from pydantic import BaseModel
from typing import Union, Optional
from constants import ERROR_MESSAGES
from passlib.context import CryptContext
from datetime import datetime, timedelta
import requests
import jwt
import logging
import config

logging.getLogger("passlib").setLevel(logging.ERROR)


JWT_SECRET_KEY = config.WEBUI_JWT_SECRET_KEY
ALGORITHM = "HS256"

##############
# Auth Utils
##############

bearer_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return (
        pwd_context.verify(plain_password, hashed_password) if hashed_password else None
    )


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    payload = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, options={"verify_signature": False})
        return decoded
    except Exception as e:
        return None


def extract_token_from_auth_header(auth_header: str):
    return auth_header[len("Bearer ") :]


def get_current_user(auth_token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    data = decode_token(auth_token.credentials)
    if data != None and "email" in data:
        user = Users.get_user_by_email(data["email"])
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGES.INVALID_TOKEN,
            )
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )
