from datetime import datetime

import utils
from revengegames.RevengeGameGenerator import RevengeGameGenerator

now = datetime.now()

def get_revenge_games_today(json_body):
    response = {}
    if json_body:
        leagues = json_body.get("leagues")
        if leagues and utils.validate_array(leagues):
            response["data"] = {}
            for league in leagues:
                if (utils.validate_league(league)):
                    revengeGameGenerator = RevengeGameGenerator(league, 2, now)
                    revenge_games = revengeGameGenerator.get_revenge_games()
                    response_array = []
                    for revenge_game in revenge_games:
                        response_array.append(revenge_game.to_object())
                    response["data"][league] = response_array
                else:
                    message = str(league) + " is not a valid league (ex: nhl)"
                    response = utils.create_error_response(500, message)
        else:
            message = "Please provide valid leagues array (ex: \"leagues\": [\"nhl\", \"nba\"]"
            response = utils.create_error_response(500, message)
    else:
        message = "The request body is not valid json!"
        response = utils.create_error_response(500, message)
    return response