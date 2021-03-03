from typing import List
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.Team import Team
from json_logic import jsonLogic
from sportsbetanalyzer import CONSTANTS
import utils

class Game:
    def __init__(self, home_team: Team, away_team: Team, metrics: List[str], rules: List[object]):
        self.home_team = home_team
        self.away_team = away_team
        self.metrics = metrics
        self.rules = rules
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
        return game_dict