"""
Module to store all of the database tables.
"""
from .buildings import buildings
from .deffect_types import deffect_types
from .deffects import deffects
from .enums import MFEnum, PTEnum
from .mark_feedback import mark_feedback
from .marks import marks
from .photos import photos
from .users_auth import users_auth
from .users import users

__all__ = [
    "buildings",
    "deffect_types",
    "deffects",
    "MFEnum",
    "PTEnum",
    "mark_feedback",
    "marks",
    "photos",
    "users_auth",
    "users",
]
