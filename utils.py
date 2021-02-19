from typing import List
from datetime import datetime

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

def validate_date(date):
    valid_date = False
    if isinstance(date, str):
        try:
            datetime.strptime(date, '%m-%d-%Y')
            valid_date = True
        except ValueError:
            print("Not a valid date..")
        
    return valid_date
