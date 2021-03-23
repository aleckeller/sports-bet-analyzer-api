from typing import List

from json_logic import jsonLogic
from sportsbetanalyzer import CONSTANTS
import utils

class Team():

    def __init__(self, name, abbreviation, metrics, roster, rules):
        self.name = name
        self.abbreviation = abbreviation
        self.metrics = metrics
        self.roster = roster
        self.rules = rules
        self.score = utils.determine_score(rules, self.to_dictionary(False))
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self, include_score=True):
        team_dict = {
            "name": self.name,
            "abbreviation": self.abbreviation
        }
        if isinstance(self.roster, List):
            json_players = []
            for player in self.roster:
                json_players.append(player.to_dictionary())
            team_dict[CONSTANTS.ROSTER] = json_players
        
        # TODO: Implement storing team data in s3 so we can use attributes for team
        # Scoring for teams will not work until above is implemented
        #metrics_dict = utils.create_metrics_object(self.metrics, self.team)
        #team_dict.update(metrics_dict)
        if include_score:
            team_dict["score"] = self.score
        return team_dict