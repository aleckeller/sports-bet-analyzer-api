from typing import List
from RevengeGamePlayer import RevengeGamePlayer
import json

class RevengeGame:
    def __init__(self, team_one: str, team_two: str, revenge_game_players: List[RevengeGamePlayer]):
        self.team_one = team_one
        self.team_two = team_two
        self.revenge_game_players = revenge_game_players
    
    def to_string(self):
        revenge_game_players_string = ""
        for revenge_game_player in self.revenge_game_players:
            revenge_game_players_string = revenge_game_players_string + revenge_game_player.to_string()
        the_string = f"""
        Game: 
        {self.team_one} vs. {self.team_two}

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
            "team_one": self.team_one,
            "team_two": self.team_two,
            "revenge_players": json_revenge_players
        }
        return game