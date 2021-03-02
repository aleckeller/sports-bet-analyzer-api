import utils

class RevengeGamePlayer():
    def __init__(self, player, current_team, previous_team_years, metrics):
        self.player = player
        self.id = player.player_id 
        self.name = player.name
        self.current_team = current_team
        self.previous_team_years = previous_team_years
        self.metrics = metrics
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self):
        player_dict = {
            "name": self.name,
            "current_team": self.current_team.name,
            "previous_team_years": self.previous_team_years
        }
        metrics_dict = utils.create_metrics_object(self.metrics, self.player)
        player_dict.update(metrics_dict)
        return player_dict