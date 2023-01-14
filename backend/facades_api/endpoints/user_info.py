# pylint: disable=too-many-arguments
"""
User info endpoint is defined here.
"""
from fastapi import APIRouter, Depends
from starlette import status

from facades_api.dto import User as UserDTO
from facades_api.schemas import UserInfoResponse
from facades_api.utils.dependencies import user_dependency

api_router = APIRouter(tags=["User data"])


@api_router.get(
    "/user_info",
    status_code=status.HTTP_200_OK,
    response_model=UserInfoResponse,
)
async def user_info(user: UserDTO = Depends(user_dependency)):
    """
    Return user information (email, name, registration time) when authorized.
    """
    return UserInfoResponse(name=user.name, email=user.email, registered_at=user.registered_at)
