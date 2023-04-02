"""
Exceptions connected with buildings.
"""

from fastapi import status
from facades_api.utils.exceptions import FacadesApiError


class TooManyBuildingsError(FacadesApiError):
    """
    Exception of too big number of buildings returned after user request.
    """

    def __init__(self, buildings: int, maximum_buildings: int):
        super().__init__()
        self.buildings = buildings
        self.maximum_buildings = maximum_buildings

    def get_status_code(self) -> int:
        """
        Return 400 Bad Request response code.
        """
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return f"Too many buildings requested: {self.buildings} with a maximum of {self.maximum_buildings}"
