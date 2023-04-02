"""
ClassificationResult DTO is defined here.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from facades_api.db.entities.enums import PTEnum
from facades_api.dto.geojson import GeometryDto


@dataclass(frozen=True)
class ClassificationResultDto:
    """
    Contains defect box, netural network confidence and defect class name.
    """

    box: tuple[float, float, float, float]
    confidence: float
    class_name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClassificationResultDto":
        """
        Construct dataclass from dictionary with `box`, `confidence` and `class_name` attributes.
        """
        return cls(data["box"], data["confidence"], data["class_name"])


@dataclass(frozen=True)
class PhotoDto:
    """
    Photo information DTO.
    """

    user: str
    angle_type: PTEnum
    point: GeometryDto
    loaded_at: datetime
    link: str
