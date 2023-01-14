"""
Logic exceptions module.
"""
from facades_api.logic.exceptions.buildings import TooManyBuildingsError
from facades_api.logic.exceptions.defects import DefectsClassificationError
from facades_api.logic.exceptions.files import FileSizeError
from facades_api.logic.exceptions.users import (
    AccessTokenExpiredError,
    AccessTokenUsedToRefreshError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserCredentialsInvalidError,
    UserExistsError,
    UserNotActiveError,
    UserNotFoundError,
)

__all__ = [
    "TooManyBuildingsError",
    "DefectsClassificationError",
    "FileSizeError",
    "AccessTokenUsedToRefreshError",
    "AccessTokenExpiredError",
    "RefreshTokenExpiredError",
    "RefreshTokenNotFoundError",
    "UserCredentialsInvalidError",
    "UserExistsError",
    "UserNotActiveError",
    "UserNotFoundError",
]
