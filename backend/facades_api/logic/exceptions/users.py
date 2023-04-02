"""
User-related exceptions are defined here.
"""
from fastapi import status

from facades_api.utils.exceptions import FacadesApiError


class UserExistsError(FacadesApiError):
    """
    Thrown on registration attempt when user with requested name or email already exists.
    """

    def __init__(self, email: str, name: str):
        super().__init__()
        self.email = email
        self.name = name

    def get_status_code(self) -> int:
        """
        Return 400 Bad Request http code.
        """
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return "User with requested name or email already exists"


class UserNotFoundError(FacadesApiError):
    """
    Thrown on login attempt when user with requested name or email does not exist.
    """

    def __init__(self, email: str, name: str | None = None):
        super().__init__()
        self.email = email
        self.name = name

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "User with given name or email does not exist"


class UserCredentialsInvalidError(FacadesApiError):
    """
    Thrown on login attempt when password hash did not match requested user password hash.
    """

    def __init__(self, login: str):
        super().__init__()
        self.login = login

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "User login failed, password does not match"


class UserNotActiveError(FacadesApiError):
    """
    Thrown on login attempt when user is not active ("banned") in the database.
    """

    def __init__(self, login: str):
        super().__init__()
        self.login = login

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "User login failed, it is not active"


class AccessTokenExpiredError(FacadesApiError):
    """
    Thrown on access request after token expiration time or if an access token was changed by refresh token.
    """

    def __init__(self, access_token: str):
        super().__init__()
        self.access_token = access_token

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Access token was provided, but it invalid (expired or was refreshed already)"


class RefreshTokenNotFoundError(FacadesApiError):
    """
    Thrown on refresh request when no refresh token for a user with a given device is found.
    """

    def __init__(self, refresh_token: str):
        super().__init__()
        self.refresh_token = refresh_token

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Refresh is not found, authorize again"


class RefreshTokenExpiredError(FacadesApiError):
    """
    Thrown on refresh request after token expiration time or if a refreh token was already refreshed.
    """

    def __init__(self, refresh_token: str):
        super().__init__()
        self.refresh_token = refresh_token

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Refresh token is expired or was refreshed already"


class AccessTokenUsedToRefreshError(FacadesApiError):
    """
    Thrown on refresh request with an access token given.
    """

    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def get_status_code(self) -> int:
        """
        Return 400 Bad Request http code.
        """
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return "Token refresh requested with access token given"
