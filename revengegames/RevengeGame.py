from typing import List
from revengegames.RevengeGamePlayer import RevengeGamePlayer
from revengegames.RevengeGameTeam import RevengeGameTeam
from json_logic import jsonLogic
from revengegames import CONSTANTS
import utils

class RevengeGame:
    def __init__(self, home_team: RevengeGameTeam, away_team: RevengeGameTeam, revenge_game_players: List[RevengeGamePlayer], metrics: List[str]):
        self.home_team = home_team
        self.away_team = away_team
        self.revenge_game_players = revenge_game_players
        self.revenge_score = 0
        self.metrics = metrics
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self):
        json_revenge_players = []
        for revenge_game_player in self.revenge_game_players:
            json_revenge_players.append(revenge_game_player.to_dictionary())

        game_dict = {
            "home_team": self.home_team.to_dictionary(),
            "away_team": self.away_team.to_dictionary(),
            "revenge_players": json_revenge_players,
            "revenge_score": self.revenge_score
        }
        metrics_dict = utils.create_metrics_object(self.metrics, game_dict)
        game_dict.update(metrics_dict)
        return game_dict
    
    def determine_revenge_score(self, json_logic):
        score = 0
        if isinstance(json_logic, List):
            for logic in json_logic:
                for logic_object in CONSTANTS.JSON_LOGIC_OBJECT_KEYS:
                    logic_object_rules = logic.get(logic_object)
                    if logic_object_rules:
                        rules = logic_object_rules.get(CONSTANTS.RULES_KEY)
                        if rules and isinstance(rules, List):
                            for rule_obj in rules:
                                rule = rule_obj.get(CONSTANTS.RULE_KEY)
                                points = rule_obj.get(CONSTANTS.POINTS_KEY)
                                # Determine what kind of logic to do based on logic_object
                                if logic_object == CONSTANTS.PLAYER_KEY:
                                    player_score = player_logic(rule, self.revenge_game_players, points)
                                    score = score + player_score
                                elif logic_object == CONSTANTS.GAME_KEY:
                                    game_score = game_logic(rule, self.to_dictionary(), points)
                                    score = score + game_score
        self.revenge_score = score
    
def player_logic(rule, players, points):
    score = 0
    for player in players:
        data = player.to_dictionary()
        if jsonLogic(rule, data):
            score = score + points
    return score

def game_logic(rule, game, points):
    score = 0
    if jsonLogic(rule, game):
        score = score + points
    return score
