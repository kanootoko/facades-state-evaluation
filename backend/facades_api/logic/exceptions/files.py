"""
Files-related exceptions are defined here.
"""
from fastapi import status

from facades_api.utils.exceptions import FacadesApiError


class FileSizeError(FacadesApiError):
    """
    Thrown on a file upload attempt if the file size is too low or too high.
    """

    def __init__(self, filesize: int):
        super().__init__()
        self.filesize = filesize

    def status_code(self) -> int:
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return "Uploaded file size is too low or too high"
