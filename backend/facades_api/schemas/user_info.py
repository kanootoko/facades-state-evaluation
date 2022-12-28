# pylint: disable=no-name-in-module, too-few-public-methods
"""
User info response is defined here.
"""
from datetime import datetime

from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    """
    Response body class for user info endpoint - contains user information.
    """

    email: str
    name: str
    registered_at: datetime
