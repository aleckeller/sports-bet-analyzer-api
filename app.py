from flask import Flask, request, jsonify
from datetime import datetime

from RevengeGameGenerator import RevengeGameGenerator
import utils

app = Flask(__name__)
now = datetime.now()

@app.route('/revenge-games-today/', methods=['POST'])
def revenge_games_today():
    json_body = request.get_json()
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
    return jsonify(response)

def create_error_response(code, message):
    return {
        "error": {
            "code": code,
            "message": message
        }
    }

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Revenge Game Generator!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)