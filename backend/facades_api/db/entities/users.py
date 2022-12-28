# pylint: disable=too-many-ancestors, abstract-method
"""
Users database table is defined here.
"""
from datetime import datetime
from typing import NamedTuple

from sqlalchemy import CHAR, TIMESTAMP, Boolean, Column, Integer, Sequence, String, Table, UniqueConstraint, func

from facades_api.db import metadata


class UsersTable(Table):
    """
    An attempt to annotate users columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "UsersColumns",
            [
                ("id", int),
                ("email", str),
                ("name", str),
                ("password_hash", str),
                ("registered_at", datetime),
                ("is_active", bool),
            ],
        )
    }


users_id_seq = Sequence("users_id_seq")


users = UsersTable(
    "users",
    metadata,
    Column("id", Integer, users_id_seq, server_default=users_id_seq.next_value(), primary_key=True),
    Column("email", String(64), nullable=False),
    Column("name", String(30), nullable=False),
    Column("password_hash", CHAR(128), nullable=False),
    Column("registered_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
    Column("is_active", Boolean, nullable=False, default=True),
    UniqueConstraint("email", name="users_unique_email"),
    UniqueConstraint("name", name="users_unique_name"),
)
