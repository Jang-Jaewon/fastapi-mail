from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from db import database
from models import RoleType, user

jwt_secret = config("JWT_SECRET")
algorithm = config("ALGORITHM")


class AuthManager:
    @staticmethod
    def encode_token(user_obj):
        try:
            payload = {
                "sub": user_obj["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }
            return jwt.encode(payload, jwt_secret, algorithm=algorithm)
        except Exception as ex:
            # Log the exception
            raise ex


class CustomHHTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, jwt_secret, algorithms=[algorithm])
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


oauth2_scheme = CustomHHTPBearer()


def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")
