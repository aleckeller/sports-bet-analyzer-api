from typing import List
from revengegames.RevengeGamePlayer import RevengeGamePlayer
from revengegames.RevengeGameTeam import RevengeGameTeam

class RevengeGame:
    def __init__(self, home_team: RevengeGameTeam, away_team: RevengeGameTeam, revenge_game_players: List[RevengeGamePlayer]):
        self.home_team = home_team
        self.away_team = away_team
        self.revenge_game_players = revenge_game_players
    
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
            "revenge_players": json_revenge_players
        }
        return game