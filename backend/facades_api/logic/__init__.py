"""
This module contains endpoints logic layer with database queries.
"""
from facades_api.logic.authorization import authorize, refresh_tokens
from facades_api.logic.buildings import get_buildings, get_buildings_in_square
from facades_api.logic.evaluation import update_evaluation_value
from facades_api.logic.registration import register
from facades_api.logic.photos import classify_defects, save_classification_results, save_photo
from facades_api.logic.user_info import get_user_info, validate_user_token
