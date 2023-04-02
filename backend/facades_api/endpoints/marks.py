# pylint: disable=too-many-arguments
"""
get_marks endpoint is defined here.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from facades_api.db.connection import get_connection
from facades_api.schemas.marks import MarkDefects, MarksGetResponse
from facades_api.logic.marks import get_photo_marks, get_mark_defects

from .routers import marks_router


@marks_router.get("/photo/{photo_id}/marks", status_code=status.HTTP_200_OK)
async def get_marks(
    photo_id: int,
    conn: AsyncConnection = Depends(get_connection),
) -> MarksGetResponse:
    """
    Get the given photo's marks list.
    """
    return MarksGetResponse.from_dto(await get_photo_marks(conn, photo_id))


@marks_router.get("/mark/{mark_id}/defects", status_code=status.HTTP_200_OK)
async def get_defects(
    mark_id: int,
    conn: AsyncConnection = Depends(get_connection),
) -> MarkDefects:
    """
    Get the given mark's defects list.
    """
    return MarkDefects.from_dto(await get_mark_defects(conn, mark_id))
