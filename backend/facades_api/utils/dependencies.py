"""
FastApi dependencies are defined here.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncConnection
from facades_api.db.connection import get_connection
from facades_api.logic import get_user_info, validate_user_token
from facades_api.dto.user import User as UserDTO
from facades_api.logic.exceptions import AccessTokenExpiredError

from facades_api.utils.tokens import Token


def access_token_dependency(access_token: OAuth2PasswordBearer(tokenUrl="/api/login") = Depends()) -> Token:
    """
    Return token constructed from JWT token given in `Authorization` header.
    """
    return Token.from_jwt(access_token)


async def user_dependency(
    access_token: Token = Depends(access_token_dependency),
    conn: AsyncConnection = Depends(get_connection),
) -> UserDTO:
    """
    Return user fetched from the database by email from a validated access token.

    Ensures that User is active and valid.
    """
    if not await validate_user_token(conn, access_token):
        raise AccessTokenExpiredError(access_token)
    return await get_user_info(conn, access_token.email)
