import utils

class Player():
    def __init__(self, player, metrics, rules):
        self.player = player
        self.id = player.player_id 
        self.name = player.name
        self.metrics = metrics
        self.rules = rules
        self.score = utils.determine_score(rules, self.to_dictionary(False))
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self, include_score=True):
        player_dict = {
            "name": self.name
        }
        metrics_dict = utils.create_metrics_object(self.metrics, self.player)
        player_dict.update(metrics_dict)
        if include_score:
            player_dict["score"] = self.score
        if getattr(self.player, "previous_team_years", None):
            player_dict["previous_team_years"] = self.player.previous_team_years
        if getattr(self.player, "current_team", None):
            player_dict["current_team"] = self.player.current_team
        if getattr(self.player, "previous_team", None):
            player_dict["previous_team"] = self.player.previous_team
        return player_dict