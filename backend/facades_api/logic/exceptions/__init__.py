"""
Logic exceptions module.
"""
from facades_api.logic.exceptions.buildings import TooManyBuildingsError
from facades_api.logic.exceptions.users import (
    AccessTokenUsedToRefreshError,
    AccessTokenExpiredError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserCredentialsInvalidError,
    UserExistsError,
    UserNotActiveError,
    UserNotFoundError,
)

__all__ = [
    "TooManyBuildingsError",
    "AccessTokenUsedToRefreshError",
    "AccessTokenExpiredError",
    "RefreshTokenExpiredError",
    "RefreshTokenNotFoundError",
    "UserCredentialsInvalidError",
    "UserExistsError",
    "UserNotActiveError",
    "UserNotFoundError",
]
