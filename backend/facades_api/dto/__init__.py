"""
DTOs (Data Transfer Objects) are defined in this module.

`DTO` is different from `model` as it is not always a database object.
And it is different from `schema` as responses and requests often have less fields than a DTO.
"""
from facades_api.dto.authorization import TokensTuple
from facades_api.dto.upload_photo import ClassificationResult
from facades_api.dto.user import User

__all__ = [
    "TokensTuple",
    "ClassificationResult",
    "User",
]
