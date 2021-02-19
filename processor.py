from datetime import datetime

import utils
from revengegames.RevengeGameGenerator import RevengeGameGenerator
from revengegames import CONSTANTS

def get_revenge_games_today(json_body):
    response = {}
    if json_body:
        leagues = json_body.get("leagues")
        if leagues and utils.validate_array(leagues):
            date = json_body.get("date")
            if date and utils.validate_date(date):
                date_object = datetime.strptime(date, '%m-%d-%Y')
                response["data"] = {}
                for league in leagues:
                    if (utils.validate_league(league)):
                        number_of_years_back = json_body.get("number_of_years_back")
                        if not number_of_years_back:
                            number_of_years_back = CONSTANTS.DEFAULT_NUMBER_OF_YEARS_BACK
                        revengeGameGenerator = RevengeGameGenerator(league, number_of_years_back, date_object)
                        revenge_games = revengeGameGenerator.get_revenge_games()
                        response_array = []
                        for revenge_game in revenge_games:
                            response_array.append(revenge_game.to_object())
                        response["data"][league] = response_array
                    else:
                        message = str(league) + " is not a valid league (ex: nhl)"
                        response = utils.create_error_response(500, message)
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