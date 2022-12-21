# pylint: disable=too-many-ancestors, abstract-method
"""
Users Authentication database table is defined here.
"""
from datetime import datetime
from typing import NamedTuple

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, Sequence, String, Table, func

from facades_api.db import metadata


class UsersAuthTable(Table):
    """
    An attempt to annotate users_auth columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "UsersAuthColumns",
            [
                ("id", int),
                ("user_id", int),
                ("device", str),
                ("is_active", bool),
                ("last_update", datetime),
            ],
        )
    }


users_auth_id_seq = Sequence("users_auth_id_seq")


users_auth = UsersAuthTable(
    "users_auth",
    metadata,
    Column("id", Integer, users_auth_id_seq, server_default=users_auth_id_seq.next_value(), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("device", String(200), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("last_update", TIMESTAMP(timezone=True), nullable=False, default=func.now()),
)
