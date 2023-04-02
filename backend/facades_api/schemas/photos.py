# pylint: disable=no-name-in-module,too-few-public-methods
"""
Photo uploading requerst and response are defined here.
"""
from datetime import datetime
from pydantic import BaseModel

from facades_api.db.entities.enums import PTEnum
from facades_api.dto.photos import PhotoDto
from facades_api.schemas.geojson import Geometry


class UploadPhotoResponse(BaseModel):
    """
    After photo is uploaded, it is sent to classifier, result is saved to the database and mark_id is returned.
    """

    photo_id: int
    classifier_mark_id: int


class Photo(BaseModel):
    """
    Photo information.
    """

    user: str
    angle_type: PTEnum
    point: Geometry | None
    loaded_at: datetime
    link: str

    @classmethod
    def from_dto(cls, dto: PhotoDto) -> "Photo":
        """
        Construct from DTO.
        """
        return cls(
            user=dto.user,
            angle_type=dto.angle_type,
            point=(Geometry.from_dto(dto.point) if dto.point is not None else None),
            loaded_at=dto.loaded_at,
            link=dto.link,
        )


class PhotosGetResponse(BaseModel):
    """
    List of photos for a building.
    """

    photos: list[Photo]

    @classmethod
    def from_dto(cls, dtos: list[PhotoDto]):
        """
        Construct from DTOs list.
        """
        return cls(photos=[Photo.from_dto(dto) for dto in dtos])
