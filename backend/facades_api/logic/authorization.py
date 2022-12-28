"""
Registration logic is defined here.
"""
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from facades_api.db.entities import users, users_auth
from facades_api.dto import TokensTuple
from facades_api.logic.exceptions import (
    AccessTokenUsedToRefreshError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserCredentialsInvalidError,
    UserNotActiveError,
    UserNotFoundError,
)
from facades_api.utils import Token, generate_tokens, hash_password


async def authorize(conn: AsyncConnection, device: str, login: str, password: str) -> TokensTuple:
    """
    Returns an access and refresh tokens for a user if user with given login (email or name)"
        exists and password hash matched
    """
    statement = select(users.c.id, users.c.email, users.c.password_hash, users.c.is_active).where(
        (users.c.name == login) | (users.c.email == login)
    )
    res = (await conn.execute(statement)).fetchone()
    if res is None:
        raise UserNotFoundError(login)
    user_id, email, password_hash, is_active = res
    if not is_active:
        raise UserNotActiveError(login)
    if hash_password(email, password) != password_hash:
        raise UserCredentialsInvalidError(login)

    access_token, refresh_token = generate_tokens(email, device)
    statement = (
        insert(users_auth)
        .values(
            user_id=user_id,
            device=device,
            is_active=True,
            valid_until=access_token.exp,
            refresh_until=refresh_token.exp,
        )
        .on_conflict_do_update(
            "users_auth_unique_user_id_device",
            set_=dict(valid_until=access_token.exp, refresh_until=refresh_token.exp, is_active=True),
        )
    )
    await conn.execute(statement)
    await conn.commit()
    return TokensTuple(access_token.to_jwt(), refresh_token.to_jwt())


async def refresh_tokens(conn: AsyncConnection, refresh_token: Token) -> TokensTuple:
    """
    Returns an access and refresh tokens for a given refresh token if it is valid and user is active
    """
    if refresh_token.type != "refresh":
        raise AccessTokenUsedToRefreshError(refresh_token.to_jwt())
    if refresh_token.exp < datetime.now(timezone.utc):
        raise RefreshTokenExpiredError(refresh_token.to_jwt())
    statement = (
        select(users_auth.c.id, users.c.is_active, users_auth.c.refresh_until)
        .select_from(users_auth)
        .join(users, users_auth.c.user_id == users.c.id)
        .where((users.c.email == refresh_token.email) & (users_auth.c.device == refresh_token.device))
    )
    res = (await conn.execute(statement)).fetchone()
    if res is None:
        raise RefreshTokenNotFoundError(refresh_token.to_jwt())
    users_auth_id, user_is_active, refresh_until = res
    if not user_is_active:
        raise UserNotActiveError(refresh_token.email)
    if refresh_until != refresh_token.exp:
        raise RefreshTokenExpiredError(refresh_token.to_jwt())

    access_token, refresh_token = generate_tokens(refresh_token.email, refresh_token.device)
    statement = (
        update(users_auth)
        .values(
            is_active=True,
            valid_until=access_token.exp,
            refresh_until=refresh_token.exp,
        )
        .where(users_auth.c.id == users_auth_id)
    )
    await conn.execute(statement)
    await conn.commit()
    return TokensTuple(access_token.to_jwt(), refresh_token.to_jwt())
