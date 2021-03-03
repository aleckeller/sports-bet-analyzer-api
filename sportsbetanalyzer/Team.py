from typing import List

from json_logic import jsonLogic
from sportsbetanalyzer import CONSTANTS
import utils

class Team():

    def __init__(self, team, metrics, roster, rules):
        self.name = team.name
        self.abbreviation = team.abbreviation
        self.team = team
        self.metrics = metrics
        self.roster = roster
        self.rules = rules
        self.score = utils.determine_score(rules, self.to_dictionary(False))
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self, include_score=True):
        json_players = []
        for player in self.roster:
            json_players.append(player.to_dictionary())

        team_dict = {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "roster": json_players
        }

        metrics_dict = utils.create_metrics_object(self.metrics, self.team)
        team_dict.update(metrics_dict)
        if include_score:
            team_dict["score"] = self.score
        return team_dict