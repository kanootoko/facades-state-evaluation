# pylint: disable=too-many-ancestors, abstract-method
"""
Users database table is defined here.
"""
from sqlalchemy import CHAR, TIMESTAMP, Boolean, Column, Integer, Sequence, String, Table, UniqueConstraint, func

from facades_api.db import metadata

users_id_seq = Sequence("users_id_seq")

users = Table(
    "users",
    metadata,
    Column("id", Integer, users_id_seq, server_default=users_id_seq.next_value(), primary_key=True),
    Column("email", String(64), nullable=False),
    Column("name", String(30), nullable=False),
    Column("password_hash", CHAR(128), nullable=False),
    Column(
        "registered_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
    ),
    Column("is_active", Boolean, nullable=False, default=True),
    UniqueConstraint("email", name="users_unique_email"),
    UniqueConstraint("name", name="users_unique_name"),
)
"""
Facades defect types.

Columns:
- `id` - user identifier, int serial
- `email` - user email address, varchar(64)
- `name` - user login name, varchar(30)
- `password_hash` - user password hashed with salt, varchar(128)
- `registrated_at` - user registration datetime, timestamptz
- `is_active` - indicates whether user account is not banned, boolean
"""
