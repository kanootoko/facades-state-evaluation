"""
Photo uploading logic is defined here.
"""
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from facades_api.config.app_settings_global import app_settings
from facades_api.db.entities import defect_types, defects, marks, photos
from facades_api.db.entities.enums import PTEnum
from facades_api.dto.upload_photo import ClassificationResult
from facades_api.logic.exceptions.defects import DefectsClassificationError


async def save_photo(
    conn: AsyncConnection, photo: bytes, user_id: int, building_id: int, angle_type: PTEnum
) -> tuple[int, bytes]:
    """
    Insert photo information to the database and save photo to disk with a name `{id}.jpg`.
    """
    statement = (
        insert(photos).values(user_id=user_id, building_id=building_id, angle_type=angle_type).returning(photos.c.id)
    )
    photo_id = (await conn.execute(statement)).scalar()
    photo_buf = BytesIO(photo)
    image = Image.open(photo_buf)
    path = Path(app_settings.photos_directory) / f"{photo_id}.jpg"
    image.save(path, quality=90)
    await conn.commit()
    return photo_id, path.read_bytes()


async def classify_defects(photo: bytes) -> list[ClassificationResult]:
    """
    Create a request to classification service and get a list of defects.
    """
    response = requests.post(app_settings.classifier_endpoint, data=photo, timeout=60)
    if response.status_code != 200 or "defects" not in (response_data := response.json()):
        raise DefectsClassificationError()
    return [ClassificationResult.from_dict(item) for item in response_data["defects"]]


async def save_classification_results(
    conn: AsyncConnection, photo_id: int, classification_results: list[ClassificationResult]
) -> int:
    """
    Add a row to `marks` table and link new `defects` enities to it. Set user_id=0 as it should be the robot account.
    Return inserted mark_id.
    """
    statement = insert(marks).values(photo_id=photo_id, user_id=0).returning(marks.c.id)
    mark_id = (await conn.execute(statement)).scalar()
    statement = select(defect_types.c.name, defect_types.c.id)
    d_t = dict((await conn.execute(statement)).fetchall())
    for result in classification_results:
        statement = insert(defects).values(
            mark_id=mark_id,
            author_id=0,
            x=result.box[0],
            y=result.box[1],
            width=result.box[2] - result.box[0],
            height=result.box[3] - result.box[1],
            type_id=d_t[result.class_name],
        )
        await conn.execute(statement)
    await conn.commit()
    return mark_id
