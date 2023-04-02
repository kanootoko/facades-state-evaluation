"""
Marks selecting/inserting logic is defined here.
"""
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncConnection

from facades_api.db.entities import defect_types, defects, marks, photos, users
from facades_api.dto import MarkDto
from facades_api.dto.marks import DefectDto
from facades_api.logic.exceptions.common import EntityNotFoundByIdError


async def get_photo_marks(conn: AsyncConnection, photo_id: int) -> list[MarkDto]:
    """
    Get marks for a photo.
    """
    statement = select(exists().where(photos.c.id == photo_id))
    if not (await conn.execute(statement)).scalar():
        raise EntityNotFoundByIdError("photo", photo_id)

    statement = select(
        marks.c.id,
        select(users.c.name).where(users.c.id == marks.c.user_id).as_scalar(),
        marks.c.parent_id,
        marks.c.added_at,
        marks.c.rating,
        marks.c.complaints,
    ).where(marks.c.photo_id == photo_id)
    print(statement)
    return [
        MarkDto(id, author, parent_id, added_at, rating, complaints)
        for id, author, parent_id, added_at, rating, complaints in await conn.execute(statement)
    ]


async def get_mark_defects(conn: AsyncConnection, mark_id: int) -> list[DefectDto]:
    """
    Get defects for a mark.
    """
    statement = select(exists().where(marks.c.id == mark_id))
    if not (await conn.execute(statement)).scalar():
        raise EntityNotFoundByIdError("mark", mark_id)

    statement = (
        select(
            select(users.c.name).where(users.c.id == defects.c.author_id).as_scalar(),
            defects.c.x,
            defects.c.y,
            defects.c.width,
            defects.c.height,
            defect_types.c.name,
        )
        .select_from(defects)
        .join(defect_types, defects.c.type_id == defect_types.c.id)
        .where(defects.c.mark_id == mark_id)
    )
    print(statement)

    return [
        DefectDto(author, x, y, width, height, type_name)
        for author, x, y, width, height, type_name in await conn.execute(statement)
    ]
