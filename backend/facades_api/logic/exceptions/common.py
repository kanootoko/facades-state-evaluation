"""
Common API exceptions are defined here.
"""
from fastapi import status

from facades_api.utils.exceptions import FacadesApiError


class EntityNotFoundByIdError(FacadesApiError):
    """
    Thrown when requested database entity is not found by id.
    """

    def __init__(self, entity: str, idx: int):
        self.entity = entity
        self.idx = idx
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 404 Not Found http code.
        """
        return status.HTTP_404_NOT_FOUND

    def __str__(self) -> str:
        return f"Requested {self.entity} with id={self.idx} was not found"
