from datetime import datetime
import pickle
import os

from sportsbetanalyzer.GameGenerator import GameGenerator
from sportsbetanalyzer import CONSTANTS
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.RevengeGame import RevengeGame
import s3_helper

class RevengeGameGenerator(GameGenerator):
    def __init__(self, league: str, years_back: int, date_of_games: datetime, json_logic: object):
        super().__init__(league, date_of_games, json_logic)
        self.years_back = years_back
    
    def get_games(self, include_odds=True):
        revenge_games = []
        games = super().get_games(include_odds)
        for game in games:
            revenge_game_object = RevengeGame(game.home_team, game.away_team, game.metrics, game.rules, game.odds, [])
            revenge_game = self.get_revenge_game(revenge_game_object, is_revenge_game=False, switched=False)
            if revenge_game:
                revenge_games.append(revenge_game)
        return revenge_games
    
    def get_revenge_game(self, game, is_revenge_game=False, switched=False):
        if not switched:
            team_one = game.home_team
            team_two = game.away_team
        else:
            team_one = game.away_team
            team_two = game.home_team
        revenge_game = None
        for num_of_years in range(0, self.years_back + 1):
            year_to_check = self.date_of_games.year - num_of_years
            roster_key = self.league + "/rosters/" + str(year_to_check) + "/" + team_two.abbreviation + ".pkl"
            file_contents = s3_helper.read_s3_object(os.environ.get("AWS_BUCKET_NAME"), roster_key)
            roster_df = pickle.loads(file_contents)
            for player in team_one.roster:
                revenge_player = roster_df.loc[roster_df['player_id'] == player.player_id]
                if not revenge_player.empty:
                    is_revenge_game = True
                    player.add_previous_team_year(year_to_check)
                    player.set_current_team_name(team_one.name)
                    player.set_previous_team_name(team_two.name)
                    game.revenge_game_players.append(player)

        if not switched:
            revenge_game = self.get_revenge_game(game, is_revenge_game, True)
        elif is_revenge_game:
            revenge_game = game
        return revenge_game