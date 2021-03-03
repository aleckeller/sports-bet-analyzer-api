from datetime import datetime
from sportsbetanalyzer.GameGenerator import GameGenerator

import utils
from sportsbetanalyzer.RevengeGameGenerator import RevengeGameGenerator
from sportsbetanalyzer import CONSTANTS

def process_games(json_body, is_revenge_games):
    response = {}
    parsed_json = check_for_json_errors(json_body)
    if not parsed_json.get(CONSTANTS.ERROR_KEY):
        leagues = parsed_json[CONSTANTS.LEAGUES_KEY]
        date_object = parsed_json[CONSTANTS.DATE_KEY]
        response[CONSTANTS.DATA_KEY] = {}
        for league in leagues:
            if (utils.validate_league(league)):
                json_logic = get_json_logic(league, leagues)
                if is_revenge_games:
                    number_of_years_back = json_body.get(CONSTANTS.YEARS_BACK_KEY)
                    if not number_of_years_back:
                        number_of_years_back = CONSTANTS.DEFAULT_NUMBER_OF_YEARS_BACK
                    generator = RevengeGameGenerator(league, number_of_years_back, date_object, json_logic)
                else:
                    generator = GameGenerator(league, date_object, json_logic)
                games = generator.get_games()
                response_array = []
                for game in games:
                    response_array.append(game.to_dictionary())
                response[CONSTANTS.DATA_KEY][league] = response_array
            else:
                message = str(league) + " is not a valid league (ex: nhl)"
                response = utils.create_error_response(500, message)
    else:
        response = parsed_json
    return response

def check_for_json_errors(json_body):
    response = {}
    if json_body:
        leagues = json_body.get(CONSTANTS.LEAGUES_KEY)
        if leagues:
            date = json_body.get(CONSTANTS.DATE_KEY)
            if date and utils.validate_date(date):
                date_object = datetime.strptime(date, CONSTANTS.DATE_FORMAT)
                response = {
                    CONSTANTS.LEAGUES_KEY: leagues,
                    CONSTANTS.DATE_KEY: date_object,
                }
            else:
                message = "Need to provide valid date in format MM-DD-YYYY (ex: 02-18-2021)"
                response = utils.create_error_response(500, message) 
        else:
            message = "Please provide valid leagues array (ex: \"leagues\": [\"nhl\", \"nba\"]"
            response = utils.create_error_response(500, message)
    else:
        message = "The request body is not valid json!"
        response = utils.create_error_response(500, message)
    return response

def get_json_logic(league, leagues):
    league_object = leagues.get(league)
    return league_object.get(CONSTANTS.JSON_LOGIC_KEY)