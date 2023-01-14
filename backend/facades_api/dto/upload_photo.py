# pylint: disable=invalid-name
"""
ClassificationResult DTO is defined here.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ClassificationResult:
    """
    Contains defect box, netural network confidence and defect class name.
    """

    box: tuple[float, float, float, float]
    confidence: float
    class_name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClassificationResult":
        """
        Construct dataclass from dictionary with `box`, `confidence` and `class_name` attributes.
        """
        return cls(data["box"], data["confidence"], data["class_name"])
