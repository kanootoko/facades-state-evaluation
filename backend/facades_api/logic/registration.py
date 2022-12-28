"""
Registration logic is defined here.
"""
from sqlalchemy import exists, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from facades_api.db.entities import users
from facades_api.logic.exceptions.users import UserExistsError
from facades_api.utils import hash_password


async def register(conn: AsyncConnection, email: str, name: str, password: str) -> None:
    """
    Register a user if the given email, login and password if email and login are both available.
    """
    statement = exists(1).where((users.c.name == name) | (users.c.email == email)).select()
    user_exists = (await conn.execute(statement)).scalar()
    if user_exists:
        raise UserExistsError(email, name)
    statement = insert(users).values(name=name, email=email, password_hash=hash_password(email, password))
    await conn.execute(statement)
    await conn.commit()
