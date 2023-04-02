"""
Mark and Defect DTOs are defined here.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DefectDto:
    """
    Mark defect DTO - a square of a defect with a given type.
    """

    author: str
    x: float  # pylint: disable=invalid-name
    y: float  # pylint: disable=invalid-name
    width: float
    height: float
    type: str


@dataclass(frozen=True)
class MarkDto:
    """
    Mark information DTO.
    """

    id: int  # pylint: disable=invalid-name
    author: str
    parent_id: int | None
    added_at: datetime
    rating: int
    complaints: int
