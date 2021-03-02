from typing import List
from revengegames.RevengeGamePlayer import RevengeGamePlayer
from revengegames.RevengeGameTeam import RevengeGameTeam
from json_logic import jsonLogic
from revengegames import CONSTANTS

class RevengeGame:
    def __init__(self, home_team: RevengeGameTeam, away_team: RevengeGameTeam, revenge_game_players: List[RevengeGamePlayer]):
        self.home_team = home_team
        self.away_team = away_team
        self.revenge_game_players = revenge_game_players
        self.revenge_score = 0
    
    def to_string(self):
        revenge_game_players_string = ""
        for revenge_game_player in self.revenge_game_players:
            revenge_game_players_string = revenge_game_players_string + revenge_game_player.to_string()
        the_string = f"""
        Game: 
        {self.away_team.name} vs. {self.home_team.name}

        Revenge Players: [
        {revenge_game_players_string}
        ]
        """
        return the_string
    
    def to_object(self):
        json_revenge_players = []
        for revenge_game_player in self.revenge_game_players:
            json_revenge_players.append(revenge_game_player.to_object())

        game = {
            "home_team_name": self.home_team.name,
            "away_team_name": self.away_team.name,
            "revenge_players": json_revenge_players,
            "revenge_score": self.revenge_score
        }
        return game
    
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
                                    game_score = game_logic(rule, self.to_object(), points)
                                    score = score + game_score
        self.revenge_score = score
    
def player_logic(rule, players, points):
    score = 0
    for player in players:
        data = player.to_object()
        if jsonLogic(rule, data):
            score = score + points
    return score

def game_logic(rule, game, points):
    score = 0
    if jsonLogic(rule, game):
        score = score + points
    return score