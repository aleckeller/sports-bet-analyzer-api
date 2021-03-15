from datetime import datetime
from sportsbetanalyzer.GameGenerator import GameGenerator
from sportsbetanalyzer import CONSTANTS
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.RevengeGame import RevengeGame

class RevengeGameGenerator(GameGenerator):
    def __init__(self, league: str, years_back: int, date_of_games: datetime, json_logic: object):
        super().__init__(league, date_of_games, json_logic)
        self.years_back = years_back
    
    def get_games(self):
        revenge_games = []
        games = super().get_games(slim_roster=True)
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
        team_one_roster = super().get_sports_reference_roster(team_one.abbreviation, self.date_of_games.year, True)
        team_two_roster = self.get_roster_within_years(team_two.abbreviation, self.years_back)
        revenge_game = None
        for player in team_one_roster.players.items():
            player_id = player[0]
            if team_two_roster.get(player_id):
                is_revenge_game = True
                player_previous_team_years = team_two_roster[player_id].get("years")
                player_metrics, player_rules = super().get_rules_and_metrics(CONSTANTS.PLAYER_KEY)
                sports_reference_player = self.get_player(player_id)
                setattr(sports_reference_player, "previous_team_years", player_previous_team_years)
                revenge_game_player = Player(sports_reference_player, player_metrics, player_rules)
                game.revenge_game_players.append(revenge_game_player)

        if not switched:
            revenge_game = self.get_revenge_game(game, is_revenge_game, True)
        elif is_revenge_game:
            revenge_game = game
        return revenge_game

    def get_roster_within_years(self, team_abbreviation, years_back):
        timeline_roster = {}
        for num_of_years in range(0, years_back + 1):
            year_to_check = self.date_of_games.year - num_of_years
            roster = super().get_sports_reference_roster(team_abbreviation, year_to_check, True)
            for player in roster.players.items():
                player_id = player[0]
                player_name = player[1]
                if player_id in timeline_roster.keys():
                    # Get player from timeline_roster and add year to array
                    years = timeline_roster[player_id]["years"]
                    years.append(year_to_check)
                    timeline_roster[player_id]["years"] = years
                else:
                    # Add player to timeline_roster and init year array
                    timeline_roster[player_id] = {
                        "name": player_name,
                        "years": [year_to_check]
                    }
        return timeline_roster