"""
All FastApi endpoints are exported from this module.
"""
from facades_api.endpoints.get_all_buildings import api_router as get_all_buildings
from facades_api.endpoints.health_check import api_router as health_check
from facades_api.endpoints.login import api_router as login
from facades_api.endpoints.redirect_to_swagger import api_router as redirect_to_swagger
from facades_api.endpoints.registration import api_router as registration
from facades_api.endpoints.upload_photo import api_router as upload_photo
from facades_api.endpoints.user_info import api_router as user_info

list_of_routes = [
    get_all_buildings,
    health_check,
    login,
    redirect_to_swagger,
    registration,
    upload_photo,
    user_info,
]


__all__ = [
    "list_of_routes",
]
