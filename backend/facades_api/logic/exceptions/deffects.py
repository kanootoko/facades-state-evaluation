"""
Deffects-related exceptions are defined here.
"""
from fastapi import status

from facades_api.utils.exceptions import FacadesApiError


class DeffectsClassificationError(FacadesApiError):
    """
    Thrown on deffects classification fail.
    """

    def status_code(self) -> int:
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return "Could not classificate the given image for deffects"
