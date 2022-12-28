# pylint: disable=too-many-arguments
"""
get_all_buildings endpoint is defined here.
"""
import typing as tp

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from facades_api.db.connection import get_connection
from facades_api.logic import get_buildings, get_buildings_in_square
from facades_api.schemas import GeoJSONResponse, crs_3857, crs_4326

api_router = APIRouter(tags=["Get buildings"])


@api_router.get(
    "/all_buildings",
    status_code=status.HTTP_200_OK,
    response_model=GeoJSONResponse,
)
async def get_all_buildings_geojson(
    crs: tp.Literal["4326", "3857"] = "4326",
    with_photos_only: bool = True,
    conn: AsyncConnection = Depends(get_connection),
):
    """
    Returns a full geojson listing of buildings downloaded from OpenStreetMap.
    """
    crs_obj = crs_4326 if crs == "4326" else crs_3857
    buildings = await get_buildings(conn, crs_obj, with_photos_only=with_photos_only)
    return GeoJSONResponse.from_list(buildings, crs=crs_obj)


@api_router.get(
    "/screen_buildings",
    status_code=status.HTTP_200_OK,
    response_model=GeoJSONResponse,
)
async def get_buildings_in_square_geojson(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    crs: tp.Literal["4326", "3857"] = "4326",
    with_photos_only: bool = True,
    conn: AsyncConnection = Depends(get_connection),
):
    """
    Returns a geojson listing of buildings which maps to orthophotoplans.
    """
    crs_obj = crs_4326 if crs == "4326" else crs_3857
    buildings = await get_buildings_in_square(
        conn, crs_obj, x=(x_min, x_max), y=(y_min, y_max), with_photos_only=with_photos_only
    )
    return GeoJSONResponse.from_list(buildings, crs=crs_obj)
