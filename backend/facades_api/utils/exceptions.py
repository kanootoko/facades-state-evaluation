# pylint: disable=method-hidden
"""
Top exceptions for a facades backend service are defined here.
"""

from fastapi import status, HTTPException


class FacadesApiError(HTTPException):
    """
    Base Facades API exception to inherit from.
    User can redefine `status_code` method and `__str__` as its value will be used in HTTPException.
    """

    def __init__(self):
        super().__init__(self.status_code(), str(self))

    def status_code(self) -> int:
        """
        Return FastApi response status for an HTTPException. Descestors should override this method,
            but it defaults to 500 - Internal Server Error.
        """
        return status.HTTP_500_INTERNAL_SERVER_ERROR
