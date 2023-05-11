"""
Classification result class is defined here
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClassificationResult:
    """
    Class box, netural network confidence and defect class name.
    """

    box: tuple[float, float, float, float]
    class_n: int
    class_name: str | None
    confidence: float | None = None

    @classmethod
    def from_yolo(
        cls,
        class_n: int,
        x: float,  # pylint: disable=invalid-name
        y: float,  # pylint: disable=invalid-name
        width: float,
        height: float,
        class_name: str | None = None,
        confidence: float | None = None,
    ):  # pylint: disable=too-many-arguments
        """
        Construct from YOLO output of center's X and Y coordinates with width and height parameters.
        """
        return cls((x - width / 2, y - height / 2, x + width / 2, y + height / 2), class_n, class_name, confidence)

    def to_yolo(self) -> tuple[int, float, float, float, float]:
        """
        Return YOLO box with center x, y, width and height instead of the left upper and right lower corners.
        """
        return (
            self.class_n,
            (self.box[0] + self.box[2]) / 2,
            (self.box[1] + self.box[3]) / 2,
            self.box[2] - self.box[0],
            self.box[3] - self.box[1],
        )

    def __str__(self) -> str:
        return "".join(
            [
                str(self.class_n),
                (f" ({self.class_name})" if self.class_name is not None else ""),
                f" {self.box[0]:.4f}:{self.box[1]:.4f} - {self.box[2]:.4f}:{self.box[3]:.4f}",
                (f" ({self.confidence * 100:.1f}%)" if self.confidence is not None else ""),
            ],
        )