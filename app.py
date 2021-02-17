from flask import Flask, request, jsonify
from datetime import datetime

from RevengeGameGenerator import RevengeGameGenerator
import CONSTANTS

app = Flask(__name__)
now = datetime.now()

@app.route('/get-revenge-games-today/', methods=['GET'])
def get_revenge_games_today():
    revengeGameGenerator = RevengeGameGenerator(CONSTANTS.NBA, 2, now)
    revenge_games = revengeGameGenerator.get_revenge_games()
    response_array = []
    for revenge_game in revenge_games:
        response_array.append(revenge_game.to_object())
    return jsonify(response_array)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Revenge Game Generator!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)