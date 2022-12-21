"""
All FastApi endpoints are exported from this module.
"""
from facades_api.endpoints.get_all_buildings import api_router as get_all_buildings
from facades_api.endpoints.health_check import api_router as health_check
from facades_api.endpoints.redirect_to_swagger import api_router as redirect_to_swagger

list_of_routes = [
    get_all_buildings,
    health_check,
    redirect_to_swagger,
]


__all__ = ["list_of_routes"]
