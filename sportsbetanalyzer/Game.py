from datetime import date, datetime
from typing import List
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.Team import Team
from json_logic import jsonLogic
from sportsbetanalyzer import CONSTANTS
import utils
from sportsbetanalyzer import sports_objects

class Game:
    def __init__(self, league: str, date_of_game: datetime, home_team: Team, away_team: Team, metrics: List[str], rules: List[object], odds: object):
        self.league = league
        self.date_of_game = date_of_game
        self.home_team = home_team
        self.away_team = away_team
        self.metrics = metrics
        self.rules = rules
        self.odds = odds
        self.score = utils.determine_score(rules, self.to_dictionary(False))
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self, include_score=True):
        game_dict = {
            "home_team": self.home_team.to_dictionary(),
            "away_team": self.away_team.to_dictionary()
        }
        metrics_dict = utils.create_metrics_object(self.metrics, game_dict)
        game_dict.update(metrics_dict)
        if include_score:
            game_dict["score"] = self.score
        game_dict["odds"] = self.odds
        game_dict["previous_head_to_heads"] = self.previous_head_to_heads()
        return game_dict
    
    def previous_head_to_heads(self):
        team_schedule_df = utils.get_schedule_from_s3(self.league, self.home_team.abbreviation)
        now_formatted = self.date_of_game.strftime("%Y-%m-%d")
        past_games_df = team_schedule_df.loc[(team_schedule_df["datetime"] < now_formatted)]
        past_games_against_current_opp = past_games_df.loc[past_games_df["opponent_abbr"] == self.away_team.abbreviation.upper()]
        
        previous_head_to_heads_stats = []
        for index, row in past_games_against_current_opp.iterrows():
            if row["result"] == "Win":
                winner = self.home_team.abbreviation
            else:
                winner = self.away_team.abbreviation
            points_allowed = sports_objects.get_sport_object(self.league, CONSTANTS.POINTS_ALLOWED)
            points_scored = sports_objects.get_sport_object(self.league, CONSTANTS.POINTS_SCORED)
            previous_head_to_heads_stats.append({
                "winner": winner,
                "date": row["datetime"].strftime("%Y-%m-%d"),
                "score": str(row[points_allowed]) + "-" + str(row[points_scored])
            })
        
        return previous_head_to_heads_stats