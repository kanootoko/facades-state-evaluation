"""
Defects-related exceptions are defined here.
"""
from fastapi import status

from facades_api.utils.exceptions import FacadesApiError


class DefectsClassificationError(FacadesApiError):
    """
    Thrown on defects classification fail.
    """

    def get_status_code(self) -> int:
        """
        Return 400 Bad Request http code.
        """
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return "Could not classificate the given image for defects"
