from typing import List
from datetime import datetime
from urllib.error import HTTPError

from json_logic import jsonLogic
from sportsbetanalyzer import CONSTANTS

import sportsbetanalyzer.sports_objects as sports_objects

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

def create_metrics_object(metrics, object):
    new_object = {}
    if metrics:
        for metric in metrics:
            value = getattr(object, metric, None)
            if value:
                new_object[metric] = value
    return new_object

def create_metrics_string(metrics, object):
    string = ""
    if metrics:
        for metric in metrics:
            value = getattr(object, metric, None)
            if value:
                string = string + metric + ": " + value + "\n"
    return string

def determine_score(rules, data):
    score = 0
    if rules and isinstance(rules, List):
        for rule_obj in rules:
            rule = rule_obj.get(CONSTANTS.RULE_KEY)
            points = rule_obj.get(CONSTANTS.POINTS_KEY)
            if jsonLogic(rule, data):
                score = score + points
    return score

def clean_key(string):
    return string.lower().replace("-", "").replace(" ", "").replace(".", "")

def shorten_state(string):
    return string.lower().replace("state", "st")

def get_teams(league, team_abbreviation=None, year=None):
    teams = sports_objects.get_sport_object(league, CONSTANTS.TEAMS)
    if teams:
        try:
            if team_abbreviation:
                team = teams()
                return team(team_abbreviation)
            elif year:
                return teams(year = year)
            else:
                print("Need to provide year or team abbreviation!")
                return None
        except HTTPError:
            if team_abbreviation:
                print(team_abbreviation + " does not have a team!")
            elif year:
                print(year + " does not have any teams!")
            else:
                print("Need to provide year or team abbreviation!")
            return None
    else:
        return None

def get_team_schedule(league, team_abbreviation):
    schedule = sports_objects.get_sport_object(league, CONSTANTS.SCHEDULE)
    if schedule:
        try:
            return schedule(team_abbreviation)
        except HTTPError:
            print(team_abbreviation + " does not have a schedule!")
            return None
    else:
        return None