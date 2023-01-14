"""
Logic exceptions module.
"""
from facades_api.logic.exceptions.buildings import TooManyBuildingsError
from facades_api.logic.exceptions.deffects import DeffectsClassificationError
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
    "DeffectsClassificationError",
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
