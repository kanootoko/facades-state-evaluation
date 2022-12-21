# pylint: disable=invalid-name, too-many-arguments
"""
buildings endpoints logic is defined here.
"""
from typing import Any

import pandas as pd
from geoalchemy2.functions import ST_AsGeoJSON
from loguru import logger
from numpy import nan
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import select

from facades_api.db.entities import buildings, photos
from facades_api.logic.exceptions import TooManyBuildingsError
from facades_api.schemas import Crs, crs_4326

MAX_BUILDINGS_RETURNED_PER_SCREEN = 2000


async def get_buildings(
    conn: AsyncConnection,
    crs: Crs,
    as_dataframe: bool = False,
    with_photos_only: bool = True,
) -> pd.DataFrame | list[dict[str, Any]]:
    """
    Return database buildings as a dataframe.
    """
    subq = (
        select(photos.c.building_id, func.count(photos.c.id).label("photos_count"))
        .group_by(photos.c.building_id)
        .subquery("pc")
    )
    statement = (
        select(
            buildings.c.id,
            buildings.c.address,
            buildings.c.building_year,
            (
                ST_AsGeoJSON(buildings.c.geometry)
                if crs == crs_4326
                else ST_AsGeoJSON(func.ST_TRANSFORM(buildings.c.geometry, crs.code))
            ).label("geometry"),
            subq.c.photos_count,
        )
        .select_from(buildings)
        .join(subq, buildings.c.id == subq.c.building_id, isouter=not with_photos_only)
    )
    logger.debug("Query: {}", statement)
    data = await conn.execute(statement)
    if as_dataframe:
        return pd.DataFrame(data).replace({nan: None})
    return list(data)


async def get_buildings_in_square(
    conn: AsyncConnection,
    crs: Crs,
    x: tuple[float, float],
    y: tuple[float, float],
    as_dataframe: bool = False,
    with_photos_only: bool = True,
) -> pd.DataFrame | list[dict[str, Any]]:
    """
    Return database buildings as a dataframe.
    """
    geometry_square = select(func.ST_SetSRID(func.ST_MakeEnvelope(x[0], y[0], x[1], y[1]), 4326).label("geometry")).cte(
        "geometry_square"
    )
    statement = select(func.count(buildings.c.id).label("count")).where(
        func.ST_Intersects(buildings.c.geometry, select(geometry_square.c.geometry))
    )
    logger.debug("Statement: {}", statement)
    buildings_count = (await conn.execute(statement)).fetchone()[0]
    if buildings_count > MAX_BUILDINGS_RETURNED_PER_SCREEN:
        raise TooManyBuildingsError(buildings_count, MAX_BUILDINGS_RETURNED_PER_SCREEN)
    subq = (
        select(photos.c.building_id, func.count(photos.c.id).label("photos_count"))
        .group_by(photos.c.building_id)
        .subquery("pc")
    )
    statement = (
        select(
            buildings.c.id,
            buildings.c.address,
            buildings.c.building_year,
            (
                ST_AsGeoJSON(buildings.c.geometry)
                if crs == crs_4326
                else ST_AsGeoJSON(func.ST_TRANSFORM(buildings.c.geometry, crs.code))
            ).label("geometry"),
            subq.c.photos_count,
        )
        .select_from(buildings)
        .join(subq, buildings.c.id == subq.c.building_id, isouter=not with_photos_only)
        .where(func.ST_Intersects(buildings.c.geometry, select(geometry_square.c.geometry)))
    )
    data = await conn.execute(statement)
    if as_dataframe:
        return pd.DataFrame(data).replace({nan: None})
    return list(data)
