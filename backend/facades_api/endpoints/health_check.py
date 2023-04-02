"""
health_check endpoint is defined here.
"""
from starlette import status

from facades_api.schemas import PingResponse


from .routers import system_router


@system_router.get("/health_check/ping", status_code=status.HTTP_200_OK)
async def health_check() -> PingResponse:
    """
    Return health check response.
    """
    return PingResponse()
