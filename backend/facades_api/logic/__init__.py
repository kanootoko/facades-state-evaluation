"""
This module contains endpoints logic layer with database queries.
"""
from facades_api.logic.buildings import get_buildings, get_buildings_in_square

__all__ = [
    "get_buildings",
    "get_buildings_in_square",
]
