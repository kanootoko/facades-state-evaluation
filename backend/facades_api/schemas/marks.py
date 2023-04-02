# pylint: disable=no-name-in-module,too-few-public-methods
"""
Marks responses are defined here.
"""
from datetime import datetime
from pydantic import BaseModel

from facades_api.dto.marks import DefectDto, MarkDto


class Mark(BaseModel):
    """
    Mark information DTO.
    """

    id: int  # pylint: disable=invalid-name
    author: str
    parent_id: int | None
    added_at: datetime
    rating: int
    complaints: int

    @classmethod
    def from_dto(cls, dto: MarkDto) -> "Mark":
        """
        Construct from DTO.
        """
        return cls(
            id=dto.id,
            author=dto.author,
            parent_id=dto.parent_id,
            added_at=dto.added_at,
            rating=dto.rating,
            complaints=dto.complaints,
        )


class MarksGetResponse(BaseModel):
    """
    Marks list for a given photo
    """

    marks: list[Mark]

    @classmethod
    def from_dto(cls, dtos: list[MarkDto]) -> "MarksGetResponse":
        """
        Construct from DTOs list.
        """
        return cls(marks=[Mark.from_dto(dto) for dto in dtos])


class Defect(BaseModel):
    """
    Mark defect - a square of a defect with a given type.
    """

    author: str
    x: float
    y: float
    width: float
    height: float
    type: str

    @classmethod
    def from_dto(cls, dto: DefectDto) -> "Defect":
        """
        Construct from DTO.
        """
        return cls(author=dto.author, x=dto.x, y=dto.y, width=dto.width, height=dto.height, type=dto.type)


class MarkDefects(BaseModel):
    """
    A list of defects stated by the author.
    """

    defects: list[Defect]

    @classmethod
    def from_dto(cls, dtos: list[DefectDto]) -> "MarkDefects":
        """
        Construct from DTOs list.
        """
        return cls(defects=[Defect.from_dto(dto) for dto in dtos])
