"""
Response schemas are defined here.
"""
from facades_api.schemas.basic_responses import OkResponse
from facades_api.schemas.geojson import Crs, Feature, GeoJSONResponse, Geometry, crs_3857, crs_4326
from facades_api.schemas.health_check import PingResponse
from facades_api.schemas.login import LoginResponse
from facades_api.schemas.registration import RegistrationRequest
from facades_api.schemas.user_info import UserInfoResponse

__all__ = [
    "OkResponse",
    "Crs",
    "Feature",
    "GeoJSONResponse",
    "Geometry",
    "crs_3857",
    "crs_4326",
    "PingResponse",
    "LoginResponse",
    "RegistrationRequest",
    "UserInfoResponse",
]
