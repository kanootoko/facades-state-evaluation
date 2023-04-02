"""
FastAPI API routers are defined here.
"""
from fastapi import APIRouter


buildings_router = APIRouter(tags=["Get buildings"])

system_router = APIRouter(tags=["Health check"])

user_data_router = APIRouter(tags=["User data"])

photos_router = APIRouter(tags=["Photos"])

marks_router = APIRouter(tags=["Marks"])

list_of_routers = [
    buildings_router,
    user_data_router,
    photos_router,
    marks_router,
    system_router,
]

__all__ = [
    "list_of_routers",
]
