# pylint: disable=too-many-arguments
"""
User info endpoint is defined here.
"""
from fastapi import Depends
from starlette import status

from facades_api.dto import User as UserDTO
from facades_api.schemas import UserInfoResponse
from facades_api.utils.dependencies import user_dependency

from .routers import user_data_router


@user_data_router.get(
    "/user_info",
    status_code=status.HTTP_200_OK,
    response_model=UserInfoResponse,
)
async def user_info(user: UserDTO = Depends(user_dependency)):
    """
    Return user information (email, name, registration time) when authorized.
    """
    return UserInfoResponse(name=user.name, email=user.email, registered_at=user.registered_at)
