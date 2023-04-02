# pylint: disable=invalid-name, too-many-arguments
"""
Evalaution update logic is defined here.
"""
from collections import defaultdict

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import func, select, update

from facades_api.db.entities import buildings, defect_types, defects, marks, photos
from facades_api.db.entities.enums import PTEnum


async def update_evaluation_value(conn: AsyncConnection, building_id: int) -> None:
    """
    Recalculate building evaluation in the database.
    """
    statement = select(func.count(photos.c.id)).where(  # pylint: disable=not-callable
        photos.c.building_id == building_id
    )
    if (await conn.execute(statement)).scalar() == 0:
        logger.warning("evaluation update requested for building {} without photos", building_id)
    building_photos = select(photos).where(photos.c.building_id == building_id).subquery("building_photos")
    statement = (
        select(building_photos.c.angle_type, defects.c.width, defects.c.height, defect_types.c.name)
        .select_from(building_photos)
        .join(marks, (marks.c.photo_id == building_photos.c.id) & (marks.c.user_id == 0), isouter=True)
        .join(defects, defects.c.mark_id == marks.c.id)
        .join(defect_types, defect_types.c.id == defects.c.type_id)
    )
    building_defects = (await conn.execute(statement)).fetchall()

    evaluation_value = get_evaluation_value_raw(building_defects)
    statement = (
        update(buildings)
        .values(evaluation=min(10.0, max(evaluation_value, 0.0)), evaluation_raw=evaluation_value)
        .where(buildings.c.id == building_id)
    )
    await conn.execute(statement)
    await conn.commit()
    logger.info("building {} new evaluation value = {}", building_id, evaluation_value)


def get_evaluation_value_raw(building_defects: list[PTEnum, int, int, str]) -> float:
    """
    Get raw evalution value depending on defects list: (angle_type, width, height, defect_type_name).
    """
    evaluation_value = (
        10 if any(d[0] == PTEnum.WIDE_RANGE for d in building_defects) else 8 if len(building_defects) == 0 else 6
    )
    count = defaultdict(lambda: 0)
    for _angle_type, _width, _height, defect_type in building_defects:
        count[defect_type] += 1
    evaluation_value -= count["bricks"] * 1.0
    evaluation_value -= min(count["wall_damage"] * 0.5, 6)
    evaluation_value -= min(count["crack"] * 0.5, 4)
    return evaluation_value
