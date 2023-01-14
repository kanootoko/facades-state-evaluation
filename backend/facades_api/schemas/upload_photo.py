# pylint: disable=no-name-in-module, too-few-public-methods
"""
Photo uploading requerst and response are defined here.
"""
from pydantic import BaseModel


class UploadPhotoResponse(BaseModel):
    """
    After photo is uploaded, it is sent to classifier, result is saved to the database and mark_id is returned.
    """

    photo_id: int
    classifier_mark_id: int
