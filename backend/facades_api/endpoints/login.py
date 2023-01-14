# pylint: disable=too-many-arguments
"""
Login (authorization) endpoint is defined here.
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from facades_api.db.connection import get_connection
from facades_api.logic import authorize, refresh_tokens as refresh
from facades_api.schemas import LoginResponse
from facades_api.utils import Token

api_router = APIRouter(tags=["User data"])


@api_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def authorize_user(
    device: str = "default",
    form_data: OAuth2PasswordRequestForm = Depends(),
    conn: AsyncConnection = Depends(get_connection),
):
    """
    Authorizes user by given username (email or name) and password if user exists and active.
    Return access and refresh tokens, which user would need to store and send
        in `Authorization` header with requests later.
    If the given device value was already set for other token of a given user, then old token is overwrited.
    """
    tokens = await authorize(conn, device, form_data.username, form_data.password)
    return LoginResponse(access_token=tokens.access, refresh_token=tokens.refresh)


@api_router.post(
    "/refresh_tokens",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def refresh_tokens(
    refresh_token: str,
    conn: AsyncConnection = Depends(get_connection),
):
    """
    Return access and refresh tokens for a given refresh token if it is valid and user is active.
    Returns access and refresh tokens, which user would need to store and send
        in `Authorization` header with requests later.
    If the given device value was already set for other token of a given user, then old token is overwrited.
    """
    token = Token.from_jwt(refresh_token)
    tokens = await refresh(conn, token)
    return LoginResponse(access_token=tokens.access, refresh_token=tokens.refresh)
