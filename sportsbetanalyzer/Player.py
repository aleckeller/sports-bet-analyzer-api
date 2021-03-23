import utils

class Player():
    def __init__(self, player_id, name, metrics, rules, player_data):
        self.player_id = player_id
        self.name = name
        self.metrics = metrics
        self.rules = rules
        self.player_data = player_data
        self.previous_team_years = []
        self.current_team_name = ""
        self.previous_team_name = ""
        self.score = utils.determine_score(rules, self.to_dictionary(False))
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self, include_score=True):
        player_dict = {
            "name": self.name,
            "previous_team_years": self.previous_team_years,
            "current_team_name": self.current_team_name,
            "previous_team_name": self.previous_team_name
        }
        metrics_dict = utils.create_metrics_object(self.metrics, self.player_data)
        player_dict.update(metrics_dict)
        if include_score:
            player_dict["score"] = self.score

        return player_dict
    
    def add_previous_team_year(self, year):
        self.previous_team_years.append(year)
    
    def set_current_team_name(self, name):
        self.current_team_name = name
    
    def set_previous_team_name(self, name):
        self.previous_team_name = name