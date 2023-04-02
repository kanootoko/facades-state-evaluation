"""
User DTO is defined here.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    """
    Full User model, but without password_hash.
    """

    id: int  # pylint: disable=invalid-name
    email: str
    name: str
    registered_at: datetime
    is_active: bool
