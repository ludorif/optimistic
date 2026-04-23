#  Copyright (c) 2025 Ludovic Riffiod
import logging
import os
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)

_SECRET_KEY = os.environ.get("SECRET_KEY", "")
_ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def create_session_token() -> tuple[str, str]:
    user_uuid = str(uuid.uuid4())
    token = jwt.encode({"sub": user_uuid}, _SECRET_KEY, algorithm=_ALGORITHM)
    return user_uuid, token


def get_current_uuid(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, _SECRET_KEY, algorithms=[_ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
