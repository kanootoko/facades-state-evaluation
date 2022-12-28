"""
Registration logic is defined here.
"""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from facades_api.db.entities import users, users_auth
from facades_api.dto import User as UserDTO
from facades_api.logic.exceptions.users import UserNotFoundError
from facades_api.utils import Token


async def get_user_info(conn: AsyncConnection, email: str) -> UserDTO:
    """
    Return the information of given user by email.
    """
    statement = select(
        users.c.id,
        users.c.name,
        users.c.registered_at,
        users.c.is_active,
    ).where((users.c.email == email))
    user = (await conn.execute(statement)).fetchone()
    if user is None:
        raise UserNotFoundError(email)
    return UserDTO(user[0], email, user[1], user[2], user[3])


async def validate_user_token(conn: AsyncConnection, token: Token) -> bool:
    """
    Check that token is not expired and active in the database. Return true if token is valid.
    """
    if token.exp < datetime.now(timezone.utc):
        return False

    statement = select(users_auth.c.valid_until).where(
        (users_auth.c.user_id == select(users.c.id).where(users.c.email == token.email).scalar_subquery())
        & (users_auth.c.device == token.device)
    )
    valid_until = (await conn.execute(statement)).fetchone()
    if valid_until is None:
        return False

    valid_until = valid_until[0]
    return valid_until == token.exp
