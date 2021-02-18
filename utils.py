from typing import List

import revengegames.sports_objects as sports_objects

def create_error_response(code: int, message: str):
    return {
        "error": {
            "code": code,
            "message": message
        }
    }

def validate_array(obj):
    return isinstance(obj, List)

def validate_league(league: str):
    return league in sports_objects.get_map().keys()
